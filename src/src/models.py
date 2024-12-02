import csv
from decimal import Decimal, getcontext
from datetime import datetime
from enum import StrEnum
import os
from pydantic import BaseModel


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cars_raw = os.path.join(BASE_DIR, 'src', 'cars_raw.txt')
cars_index = os.path.join(BASE_DIR, 'src', 'cars_index.txt')
cars_txt = os.path.join(BASE_DIR, 'src', 'cars.txt')
models_raw = os.path.join(BASE_DIR, 'src', 'models_raw.txt')
models_index = os.path.join(BASE_DIR, 'src', 'models_index.txt')
models_txt = os.path.join(BASE_DIR, 'src', 'models.txt')
sales_raw = os.path.join(BASE_DIR, 'src', 'sales_raw.txt')
sales_index = os.path.join(BASE_DIR, 'src', 'sales_index.txt')
sales_txt = os.path.join(BASE_DIR, 'src', 'sales.txt')


class CarStatus(StrEnum):
    available = "available"
    reserve = "reserve"
    sold = "sold"
    delivery = "delivery"


class FileHandler(BaseModel):

    def __init__(self, file_path):
        self.file_path = file_path

    def read_file_by_lines(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                yield line.strip()

    def write_line(file_path, mode, line_number, content, padding=500):
        with open(file_path, mode) as f:
            f.seek(line_number * padding)
            f.write(content.ljust(padding))

    def read_line(file_path, line_number, padding=500):
        with open(file_path, 'r') as f:
            f.seek(line_number * padding)
            return f.read(500)

    def parse_csv_line(line, delimiter='\t'):
        line_2 = line.strip(' ')
        return list(csv.reader([line_2], delimiter=delimiter))[0]


class Model(BaseModel):
    id: int
    name: str
    brand: str

    def list_models(file_path):
        all_models = []
        for i, new_line in enumerate(FileHandler.read_file_by_lines(file_path), start=1):
            if i == 1:
                continue
            parse_line = FileHandler.parse_csv_line(new_line)
            id = int(parse_line[0])
            name = parse_line[1]
            brand = parse_line[2]
            model_list = (id, name, brand)
            all_models.append(model_list)
        return all_models

    def find_model(num_str):
        line_model_index = FileHandler.read_line(models_index, num_str)
        parse_line = FileHandler.parse_csv_line(line_model_index)
        num_str_model = int(parse_line[1])-1  # Поиск номера строки в индексе
        # Поиск по номеру строки id в models.txt
        line_model = FileHandler.read_line(models_txt, num_str_model)
        parse_line_model = FileHandler.parse_csv_line(line_model)
        id = parse_line_model[0]
        model = parse_line_model[1]
        brand = parse_line_model[2]
        return id, model, brand

    def index(self) -> str:
        return str(self.id)


class Car(BaseModel):
    vin: str
    model: int
    price: Decimal
    date_start: datetime
    status: CarStatus

    def list_cars(file_path):
        all_cars = []
        for i, new_line_2 in enumerate(FileHandler.read_file_by_lines(file_path), start=1):
            if i == 1:
                continue
            parse_line_2 = FileHandler.parse_csv_line(new_line_2)
            vin = parse_line_2[0]
            model = int(parse_line_2[1])
            getcontext().prec = 8
            price = parse_line_2[2]
            price = Decimal(price)
            date_start = datetime.strptime(parse_line_2[3], '%Y-%m-%d')
            status = CarStatus(parse_line_2[4])
            car_list = (vin, model, price, date_start, status)            
            all_cars.append(car_list)
        return all_cars

    def find_vin(num_str):
        line_cars_index = FileHandler.read_line(cars_index, num_str)
        parse_line = FileHandler.parse_csv_line(line_cars_index)
        num_str_cars = int(parse_line[1])-1  # Поиск номера строки в индексе
        # Поиск по номеру строки vin в cars.txt
        line_cars = FileHandler.read_line(cars_txt, num_str_cars)
        parse_line_cars = FileHandler.parse_csv_line(line_cars)
        vin = parse_line_cars[0]
        return vin, num_str_cars, parse_line_cars

    def index(self) -> str:
        return self.vin


class Sale(BaseModel):
    sales_number: str
    car_vin: str
    sales_date: datetime
    cost: Decimal

    def list_sales(file_path):
        all_sales = []
        for i, new_line_3 in enumerate(FileHandler.read_file_by_lines(file_path), start=1):
            if i == 1:
                continue
            parse_line_3 = FileHandler.parse_csv_line(new_line_3)
            sales_number = parse_line_3[0]
            car_vin = parse_line_3[1]
            getcontext().prec = 5
            cost = Decimal(parse_line_3[2])
            sales_date = datetime.strptime(parse_line_3[3], '%Y-%m-%d')
            is_deleted = 'False'
            sale_list = (sales_number, car_vin, cost, sales_date, is_deleted)            
            all_sales.append(sale_list)
        return all_sales

    def find_vin_sales(num_str):
        line_index = FileHandler.read_line(sales_index, num_str)
        parse_line = FileHandler.parse_csv_line(line_index)
        num_str_sales = int(parse_line[1])-1  # Поиск номера строки в индексе
        # Поиск по номеру строки vin в продажах
        line_sales = FileHandler.read_line(sales_txt, num_str_sales)
        parse_line_sales = FileHandler.parse_csv_line(line_sales)
        sales_vin = parse_line_sales[1]
        return sales_vin, parse_line_sales

    def index(self) -> str:
        return str(self.id)


class CarFullInfo(BaseModel):
    vin: str
    car_model_name: str
    car_model_brand: str
    price: Decimal
    date_start: datetime
    status: CarStatus
    sales_date: datetime | None
    sales_cost: Decimal | None


class ModelSaleStats(BaseModel):
    car_model_name: str
    brand: str
    sales_number: int
