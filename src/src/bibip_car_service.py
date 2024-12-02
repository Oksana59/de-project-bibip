import csv
from decimal import Decimal, getcontext
from datetime import datetime
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
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


class CarService:

    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        for i, new_line in enumerate(list_all_models):
            id, model, brand = new_line
            line = str(id) + '\t' + str(model) + '\t' + str(brand)
            FileHandler.write_line(models_txt, 'a', i, line)

        for j, new_line_2 in enumerate(list_all_models, start=1):
            id = new_line_2[0]
            line_2 = str(id) + '\t' + str(j)
            FileHandler.write_line(models_index, 'a', j, line_2)
        return

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        for i, new_line_3 in enumerate(list_all_cars):
            vin, model, price, date_start, status = new_line_3
            line_3 = vin + '\t' + str(model) + '\t' + str(price) + '\t' + str(date_start)+ '\t' + str(status)
            FileHandler.write_line(cars_txt, 'a', i, line_3)

        for j, new_line_4 in enumerate(list_all_cars, start=1):
            vin = new_line_4[0]
            line_4 = vin + '\t' + str(j)
            FileHandler.write_line(cars_index, 'a', j, line_4)
        return

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        for i, new_line_5 in enumerate(list_all_sales):
            sales_number, car_vin, cost, sales_date, is_deleted = new_line_5
            line_5 = sales_number + '\t' + car_vin + '\t' + str(cost) + '\t' + str(sales_date) + '\t' + str(is_deleted)
            FileHandler.write_line(sales_txt, 'a', i, line_5)

        for j, new_line_6 in enumerate(list_all_sales, start=1):
            car_vin = new_line_6[1]
            line_6 = car_vin + '\t' + str(j)
            FileHandler.write_line(sales_index, 'a', j, line_6)

        # Изменение статуса в cars.txt
        i = 0
        while True:
            line_index = FileHandler.read_line(sales_index, i)
            if line_index == '':
                break
            sales_vin, parse_line_sales = Sale.find_vin_sales(i)  # Поиск vin в продажах
            j = 0
            while True:  # Поиск информации в cars_index.txt
                line_cars_index = FileHandler.read_line(cars_index, j)
                if line_cars_index == '':
                    break
                vin, num_str_cars, parse_line_cars = Car.find_vin(j)
                if sales_vin == vin:
                    # Создание строки для замены статуса и перезапись в файл cars.txt
                    new_str = str(parse_line_cars[0]) + '\t' + str(parse_line_cars[1]) + '\t' + str(parse_line_cars[2]) + '\t' + str(parse_line_cars[3]) + '\t' + 'sold'
                    FileHandler.write_line(cars_txt, 'r+', num_str_cars, new_str)
                    break
                j += 1
            i += 1
        return
    
    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        car_list_available = []
        i = 0
        while True:
            line_car = FileHandler.read_line(cars_txt, i)
            if line_car == '':
                break
            parse_line = FileHandler.parse_csv_line(line_car)
            status_car = parse_line[4]
            if status_car == status:
                car_list_available.append(parse_line)
            i += 1
        car_list_available = sorted(car_list_available, key=lambda x: x[0])  # Сортировка по vin
        return
    
    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        i = 0
        while True:
            line_cars_index = FileHandler.read_line(cars_index, i)
            if line_cars_index == '':
                break
            vin, num_str_cars, parse_line_cars = Car.find_vin(i)
            getcontext().prec = 8
            price = parse_line_cars[2]
            price = Decimal(price)
            date_start = datetime.strptime(parse_line_cars[3], '%Y-%m-%d  %H:%M:%S')
            status = CarStatus(parse_line_cars[4])
            model_car_id = parse_line_cars[1]

            # Поиск информации в models
            j = 0
            while True:
                line_cars_index = FileHandler.read_line(models_index, j)
                if line_cars_index == '':
                    break
                id_model, model, brand = Model.find_model(j)
                if model_car_id == id_model:
                    model_name = model
                    model_brand = brand
                    break
                j += 1

            # Поиск информации в sales если статус = 'sold'
            status_car = parse_line_cars[4]
            if status_car == 'sold':
                h = 0
                while True:
                    line_sales_index = FileHandler.read_line(sales_index, h)
                    if line_sales_index == '':
                        break
                    sales_vin, parse_line_sales = Sale.find_vin_sales(h)
                    if vin == sales_vin:
                        sales_date = datetime.strptime(parse_line_sales[3], '%Y-%m-%d  %H:%M:%S')
                        sales_cost = parse_line_sales[2]
                        break
                    h += 1
            else:
                sales_cost = 'None'
                sales_date = 'None'
            # Добавление информации об автомобиле в итоговый объект
            CarFullInfo = (f'vin  {vin}\nmodel  {model_name}\nmodel_brand  {model_brand}\nprice   {price}\n'
                f'date_start  {date_start}\nstatus  {status_car}\nsales_date  {sales_date}\nsales_cost  {sales_cost}')
            break
        print(CarFullInfo)
        return CarFullInfo

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        i = 0
        while True:
            line_cars_index = FileHandler.read_line(cars_index, i)
            if line_cars_index == '':
                break
            car_vin, num_str_cars, parse_line_cars = Car.find_vin(i)
            if car_vin == vin:
                # Замена vin в таблице cars.txt
                new_str = new_vin + '\t' + str(parse_line_cars[1]) + '\t' + str(parse_line_cars[2]) + '\t' + str(parse_line_cars[3]) + '\t' + str(parse_line_cars[4])
                FileHandler.write_line(cars_txt, 'r+', i, new_str)
                # Замена vin в таблице cars_index.txt
                new_str_index = new_vin + '\t' + str(i+1)
                FileHandler.write_line(cars_index, 'r+', i, new_str_index)
                break
            i += 1
        return
    
    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        i = 0
        while True:
            line_sales = FileHandler.read_line(sales_txt, i)
            if line_sales == '':
                break
            sales_vin, parse_line_sales = Sale.find_vin_sales(i)
            number_sale_file = parse_line_sales[0]
            if sales_number == number_sale_file:
                new_line_sale = sales_number + '\t' + parse_line_sales[1] + '\t' + parse_line_sales[2] + '\t' + parse_line_sales[3] + '\t' + 'True'
                FileHandler.write_line(sales_txt, 'r+', i, new_line_sale)
                break
            i += 1
        return
    
    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        model_dict = {}
        i = 0
        while True:  # Поиск vin в sales
            line_index = FileHandler.read_line(sales_txt, i)
            if line_index == '':
                break
            sales_vin, parse_line_sales = Sale.find_vin_sales(i)

            j = 0
            while True:  # Поиск информации в cars
                line_cars_index = FileHandler.read_line(cars_index, j)
                if line_cars_index == '':
                    break
                vin, num_str_cars, parse_line_cars = Car.find_vin(j)
                if vin == sales_vin:  # Условие сопоставления vin 
                    car_model_id = parse_line_cars[1]

                    h = 0
                    while True:  # Поиск информации в models.txt
                        line_model_index = FileHandler.read_line(models_index, h)
                        if line_model_index == '':
                            break
                        id, car_model_name, brand = Model.find_model(h)
                        if car_model_id == id:
                            getcontext().prec = 8
                            price = Decimal(parse_line_sales[2])
                            # Запись двух значений в список для добавления в словарь
                            new_list = []
                            new_list.append(1)
                            new_list.append(price)
                            new_list.append(brand)
                            if car_model_name not in model_dict:
                                model_dict[car_model_name] = new_list  # Добавление значения для новой модели
                            else:
                                model_dict[car_model_name][0] += 1
                                model_dict[car_model_name][1] += price  # Прибавление значений к уже добавленной модели
                            break
                        h += 1
                    break
                j += 1
            i += 1
        model_dict_sorted = sorted(model_dict.items(), key=lambda item:item[1],  reverse=True)  # Сортировка
        top_3_models_by_sales = model_dict_sorted[0:3]   # Выбор первых трех в отсортированном списке
        first_model = f'{top_3_models_by_sales[0][0]}  {top_3_models_by_sales[0][1][2]}  {top_3_models_by_sales[0][1][0]}'
        second_model = f'{top_3_models_by_sales[1][0]}  {top_3_models_by_sales[1][1][2]}  {top_3_models_by_sales[1][1][0]}'
        third_model = f'{top_3_models_by_sales[2][0]}  {top_3_models_by_sales[2][1][2]}  {top_3_models_by_sales[2][1][0]}'
        ModelSaleStats = [first_model, second_model, third_model]
        print(ModelSaleStats)
        return ModelSaleStats


# Задание 1
list_all_models = Model.list_models(models_raw)
Service_model = CarService(root_directory_path=models_txt)
Service_model.add_model(list_all_models)

list_all_cars = Car.list_cars(cars_raw)
Service_car = CarService(root_directory_path=cars_txt)
Service_car.add_car(list_all_cars)

# Задание 2
list_all_sales = Sale.list_sales(sales_raw)
Service_sale = CarService(root_directory_path=sales_txt)
Service_sale.sell_car(list_all_sales)

# Задание 3
Service_car.get_cars(status='available')

# Задание 4
Service_car = CarService(root_directory_path=cars_txt)
Service_car.get_car_info(input('Введите vin '))

# Задание 5
Service_car = CarService(root_directory_path=cars_txt)
Service_car.update_vin('KNAGH4A48A5414970', 'KNAGH4A48A5414971')

# Задание 6
Service_sale = CarService(root_directory_path=sales_txt)
Service_sale.revert_sale('20240903#KNAGH4A48A5414970')

# Задание 7
Service_sale = CarService(root_directory_path=sales_txt)
Service_sale.top_models_by_sales()
