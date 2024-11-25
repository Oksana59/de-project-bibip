from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from decimal import Decimal, getcontext 
import linecache


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # Добавление моделей и индексов в текстовые файлы
        i = 1
        while True:
            # Чтение из файла исходника с моделями
            new_line = linecache.getline('C:\Dev\de-project-bibip\src\models_raw.txt', i).strip(' ')
            if new_line != '':
                # Запись строки из исходника в models.txt
                with open('C:\Dev\de-project-bibip\src\models.txt', 'a') as f:
                    f.seek(i*500)  # первое число - номер строки
                    f.write(new_line.ljust(500))
                    st = new_line.split('\t')
                    key_v = st[0]
                # Запись строки из исходника в models_index.txt
                with open('C:\Dev\de-project-bibip\src\models_index.txt', 'a') as f:
                    if i == 1:
                        line = key_v + ' ' + 'index'  # Добавление поля с номером строки
                    else:
                        line = key_v + ' ' + str(i-1)
                    f.seek(i*500)
                    f.write(line.ljust(500))
                i += 1
            else:
                break


    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        # Добавление автомобилей и индексов в текстовые файлы
        i = 1
        while True:
            # Чтение из файла исходника с автомобилями
            new_line = linecache.getline('C:\Dev\de-project-bibip\src\cars_raw.txt', i).strip(' ')
            if new_line != '':
                # Запись строки из исходника в cars.txt
                with open('C:\Dev\de-project-bibip\src\cars.txt', 'a') as f:
                    f.seek(i*500)  # первое число - номер строки
                    f.write(new_line.ljust(500))
                    st = new_line.split('\t')
                    key_v = st[0]
                # Запись строки из исходника в cars_index.txt
                with open('C:\Dev\de-project-bibip\src\cars_index.txt', 'a') as f:
                    if i == 1:
                        line = key_v + ' ' + 'index'  # Добавление поля с номером строки
                    else:
                        line = key_v + ' ' + str(i-1)
                    f.seek(i*500)
                    f.write(line.ljust(500))
                i += 1
            else:
                break


    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        # Добавление продаж и индексов в текстовые файлы
        i = 1
        while True:
            # Чтение из файла выгрузки продаж (исходник)
            new_line = linecache.getline('C:\Dev\de-project-bibip\src\sales_raw.txt', i).strip(' ')
            if new_line != '':
                # Запись продажи в sales.txt
                with open('C:\Dev\de-project-bibip\src\sales.txt', 'a') as f:
                    f.seek(i*500)  # первое число - номер строки
                    f.write(new_line.ljust(500))
                    # Поиск vin и запись в индекс продаж
                    st = new_line.split('\t')
                    key_v = st[1]
                with open('C:\Dev\de-project-bibip\src\sales_index.txt', 'a') as f:
                    if i == 1:
                        line = key_v + ' ' + 'index'  # Добавление строки заголовка с полем индекса
                    else:
                        line = key_v + ' ' + str(i-1)  # Добавление номера строки
                    f.seek(i*500)
                    f.write(line.ljust(500))
                i += 1
            else:
                break

        # Чтение записей из индекса для поиска строк
        i = 1
        while True:
            with open('C:\Dev\de-project-bibip\src\sales_index.txt', 'r') as f:
                f.seek(i*500) 
                val = f.read(500)
            # Условие выхода из внешнего цикла while
            if val == '':
                break
            else:
                val = val.split(' ')
                num_str = int(val[1])  # Поиск номера строки в индексе
                # Чтение по номеру строки из файла с продажами
                new_line = linecache.getline('C:\Dev\de-project-bibip\src\sales.txt', num_str+1).strip(' ')
                new_line = new_line.replace('\n', '')
                new_line = new_line.strip(' ')
                new_line = new_line.split('\t')
                vin = new_line[1] # Поиск vin в таблице продаж

                # Чтение и поиск по vin в индексе автомобилей номера строки
                j = 1
                while True:   
                    with open('C:\Dev\de-project-bibip\src\cars_index.txt', 'r') as f:
                        f.seek(j*500) 
                        val2 = f.read(500)
                    # Условие выхода из вложенного цикла while
                    if val2 == '':
                        break
                    else:
                        val2 = val2.split(' ')
                        vin2 = val2[0]  # Поиск vin в таблице автомобилей
                        num_str2 = int(val2[1])  # Поиск номера строки для чтения в файле автомобилей
                        # Условие поиска по vin, если найден статуc меняется на sold
                        if vin == vin2:
                            new_line2 = linecache.getline('C:\Dev\de-project-bibip\src\cars.txt', num_str2+1).strip(' ')
                            new_line2 = new_line2.replace('\n', '')
                            new_line2 = new_line2.strip(' ')
                            new_list = new_line2.split('\t')
                            # Создание строки для замены статуса и перезапись в файл cars.txt
                            new_str = str(new_list[0]) + '	' + str(new_list[1]) + '	' + str(new_list[2]) + '	' + str(new_list[3]) + '	' + 'sold' + '\n'
                            with open('C:\Dev\de-project-bibip\src\cars.txt', 'r+') as f2:
                                f2.seek((num_str2)*500) 
                                f2.write(new_str.ljust(450, ' '))
                            break
                    j += 1    
            i += 1


    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        # Создание списка со словарями авто tabl_auto
        i = 1
        new_line = 'a'
        tabl_auto = []
        while True:
            # Извлечение и преобразование данных из файла с автомобилями
            new_line = linecache.getline('C:\Dev\de-project-bibip\src\cars.txt', i).strip(' ')
            new_line = new_line.replace('\n', '')
            new_line = new_line.strip(' ')
            l = len(new_line.split('\t'))
            # Условие прерывания цикла While
            if new_line == '':
                break
            # Создание списка заголовков
            if i == 1:
                head = new_line.split('\t')
            # Вставка строк с машинами в словарь, а затем в список словарей
            if i >= 2:
                st = new_line.split('\t')
                new_dict = {}
                for j in range(l):
                    new_dict[head[j]] = st[j]  # Добавление в словарь информации об автомобиле
                # Вставка машин в список
                tabl_auto.append(new_dict)  # Добавление в список словарей с автомобилями
            i += 1

        # Отбор авто в статусе available
        list_auto = []
        for j in range(len(tabl_auto)):
            auto = tabl_auto[j]
            if auto['status'] == 'available':
                list_auto.append(auto)
            newlist = sorted(list_auto, key=lambda d: d['vin'])  # Сортировка по vin

        # Создание и печать строки заголовков полей
        kl = list(dict.keys(newlist[0]))
        kl = str(kl).replace("', '", ' ')
        kl = kl.replace("['", '')
        kl = kl.replace("']", '')
        with open('C:\Dev\de-project-bibip\src\cars_available.txt', 'a') as f:
            f.write(kl.ljust(500))

        # Вывод списка автомобилей в текстовом формате
        for i in range(len(newlist)):
            auto = list(dict.values(newlist[i]))
            auto = str(auto).replace("', '", ' ')
            auto = auto.replace("['", '')
            auto = auto.replace("']", '')
            with open('C:\Dev\de-project-bibip\src\cars_available.txt', 'a') as f:
                f.write(auto.ljust(500))

        return newlist


    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        car = input('Введите vin ')  # Ввод пользователем vin номера
        # Поиск информации в справочнике автомобилей
        j = 1
        while True:   
            with open('C:\Dev\de-project-bibip\src\cars_index.txt', 'r') as f:
                f.seek(j*500) 
                val = f.read(500)
            # Условие выхода из цикла while
            if val == '':
                break
            else:
                val = val.split(' ')
            # Определение vin и поиск номера строки при условии совпадения vin и car
                vin = val[0]
                if vin != car:
                    j += 1
                    continue
                else:
                    num_str = int(val[1])
                    # Поиск информации в файле с автомобилями по номеру строки
                    new_line = linecache.getline('C:\Dev\de-project-bibip\src\cars.txt', num_str+1).strip(' ')
                    new_line = new_line.replace('\n', '')
                    new_line = new_line.strip(' ')
                    # Создание списка и переменных с информацией по авто
                    new_list = new_line.split('\t')
                    model = new_list[1]
                    price = new_list[2]
                    date_start = new_list[3]
                    status = new_list[4]

                    # Поиск информации в справочнике моделей
                    i = 1
                    while True:   
                        with open('C:\Dev\de-project-bibip\src\models_index.txt', 'r') as f:
                            f.seek(i*500) 
                            val2 = f.read(500)
                        # Условие выхода из вложенного цикла while
                        if val2 == '':
                            break
                        # Поиск model в справочнике моделей по номеру строки
                        else:
                            val2 = val2.split(' ')
                            model2 = val2[0]
                            num_str2 = int(val2[1])
                            if model == model2:
                                new_line2 = linecache.getline('C:\Dev\de-project-bibip\src\models.txt', num_str2+1).strip(' ')
                                new_line2 = new_line2.replace('\n', '')
                                new_line2 = new_line2.strip(' ')
                                # Создание списка и переменных с информацией по авто и выход из вложенного цикла
                                new_list2 = new_line2.split('\t')
                                model_name = new_list2[1]
                                model_brand = new_list2[2]
                                break
                            else:
                                i += 1

                    # Условие определения продажи автомобиля
                    if status == 'sold':
                        # Поиск информации в таблице продаж по vin
                        h = 2
                        while True:   
                            new_line3 = linecache.getline('C:\Dev\de-project-bibip\src\sales.txt', h).strip(' ')
                            val3 = new_line3.replace('\n', '')
                            if val3 == '':
                                break
                            # Создание списка и переменных с информацией по авто и выход из вложенного цикла
                            else:
                                new_list3 = val3.split('\t')
                                vin3 = new_list3[1]
                                if vin == vin3:
                                    new_list3 = val3.split('\t')
                                    sales_cost = new_list3[2]
                                    sales_date = new_list3[3]
                                    break
                                else:
                                    h += 1
                    else:
                        sales_cost = 'None'
                        sales_date = 'None'

                # Добавление информации об автомобиле в итоговый объект
                CarFullInfo = (f'vin  {vin}\nmodel  {model}\nmodel_brand  {model_brand}\nprice   {price}\n'
                    f'date_start  {date_start}\nstatus  {status}\nsales_date  {sales_date}\nsales_cost  {sales_cost}')
                break
        return CarFullInfo


    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        wrong_vin = '5XYPH4A10GG021831'
        new_vin = '5XYPH4A10GG021832'

        # Поиск информации в справочнике автомобилей
        i = 1
        while True:   
            with open('C:\Dev\de-project-bibip\src\cars_index.txt', 'r') as f:
                f.seek(i*500) 
                val = f.read(500)
            # Условие выхода из цикла while
            if val == '':
                break
            else:
                val = val.split(' ')
            # Определение vin и поиск номера строки при условии совпадения vin и car
                vin = val[0]
                if vin != wrong_vin:
                    i += 1
                    continue
                else:
                    num_str = int(val[1])
                    # Поиск информации в файле с автомобилями по номеру строки
                    new_line = linecache.getline('C:\Dev\de-project-bibip\src\cars.txt', num_str+1).strip(' ')
                    new_line = new_line.replace('\n', '')
                    new_line = new_line.strip(' ')
                    new_list = new_line.split('\t')

                    # Замена vin в таблице cars.txt
                    new_str = str(new_vin) + '	' + str(new_list[1]) + '	' + str(new_list[2]) + '	' + str(new_list[3]) + '	' + str(new_list[4]) + '\n'
                    with open('C:\Dev\de-project-bibip\src\cars.txt', 'r+') as f2:
                        f2.seek((num_str)*500) 
                        f2.write(new_str.ljust(500, ' '))

                    # Замена vin в таблице cars_index.txt
                    new_str = str(new_vin) + '	' + str(num_str) + '\n'
                    with open('C:\Dev\de-project-bibip\src\cars_index.txt', 'r+') as f2:
                        f2.seek(num_str*500)
                        f2.write(new_str.ljust(500))
                    break
      

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        # Для добавления флага is_deleted в таблицу sales я обновила заголовок и информацию по отмененной сделке
        # для остальных строк я решила оставить этот флаг пустым, чтобы был меньше объем перезаписываемых строк
        revert_sale = '20240903#KNAGM4A77D5316538'

        # Добавление нового заголовка с полем is_deleted в таблицу sales
        new_line = linecache.getline('C:\Dev\de-project-bibip\src\sales.txt', 1).strip(' ')
        new_line = new_line.replace('\n', '')
        new_line = new_line.strip(' ')
        new_str = new_line + '\tis_deleted\n'

        # Замена заголовка в таблице sales.txt
        with open('C:\Dev\de-project-bibip\src\sales.txt', 'r+') as f2:
            f2.seek(0*500) 
            f2.write(new_str.ljust(500, ' '))

        # Поиск информации в таблице sales_index по отмененной продаже
        i = 1
        while True:   
            with open('C:\Dev\de-project-bibip\src\sales_index.txt', 'r') as f:
                f.seek(i*500) 
                val = f.read(500)
            # Условие выхода из цикла while
            if val == '':
                break
            else:
                val = val.split(' ')
            # Поиск sales_number и номера строки 
                sales_number = val[0]
                if sales_number != revert_sale:
                    i += 1
                    continue
                else:
                    num_str = int(val[1])
                    # Поиск информации в файле с продажами по номеру строки
                    new_line = linecache.getline('C:\Dev\de-project-bibip\src\sales.txt', num_str).strip(' ')
                    new_line = new_line.replace('\n', '')
                    new_line = new_line.strip(' ')
                    new_list = new_line.split('\t')

                    # Замена строки в таблице sales.txt
                    new_str = str(new_list[0]) + '	' + str(new_list[1]) + '	' + str(new_list[2]) + '	' + str(new_list[3]) + '	' + '\t' + 'True' + '\n'
                    with open('C:\Dev\de-project-bibip\src\sales.txt', 'r+') as f2:
                        f2.seek((num_str)*500) 
                        f2.write(new_str.ljust(500, ' '))
                    break



    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        i = 2
        new_line = 'a'
        model_dict = {}

        while True:
            # Извлечение и преобразование данных из файла с продажами
            new_line = linecache.getline('C:\Dev\de-project-bibip\src\sales.txt', i).strip(' ')
            new_line = new_line.replace('\n', '')
            new_line = new_line.strip(' ')
            # Условие прерывания цикла While
            if new_line == '':
                break
            st = new_line.split('\t')
            vin = st[1]  # Поиск vin в таблице продаж

            # Чтение и поиск по vin в индексе автомобилей номера строки
            j = 1
            while True:   
                with open('C:\Dev\de-project-bibip\src\cars_index.txt', 'r') as f:
                    f.seek(j*500) 
                    val2 = f.read(500)
                # Условие выхода из вложенного цикла while
                if val2 == '':
                    break
                else:
                    val2 = val2.split(' ')
                    vin2 = val2[0]  # Поиск vin в таблице автомобилей
                    num_str2 = int(val2[1])  # Поиск номера строки для чтения в файле автомобилей
                    # Условие поиска по vin
                    if vin == vin2:
                        new_line2 = linecache.getline('C:\Dev\de-project-bibip\src\cars.txt', num_str2+1).strip(' ')
                        new_line2 = new_line2.replace('\n', '')
                        new_line2 = new_line2.strip(' ')
                        new_list = new_line2.split('\t')
                        l = len(new_line.split('\t'))                
                        # Определение модели и цены продажи
                        model = new_list[1]

                        # Поиск информации в справочнике моделей
                        h = 1
                        while True:  
                            # Чтение файла индекса для поиска по id номера строки
                            with open('C:\Dev\de-project-bibip\src\models_index.txt', 'r') as f:
                                f.seek(h*500) 
                                val3 = f.read(500)
                            # Условие выхода из вложенного цикла while
                            if val3 == '':
                                break
                            # Поиск model в справочнике моделей по номеру строки
                            else:
                                val3 = val3.split(' ')
                                model3 = val3[0]
                                num_str3 = int(val3[1])
                                if model == model3:  # Если модель найдена в индексе, ищем строку в таблице с моделями
                                    new_line3 = linecache.getline('C:\Dev\de-project-bibip\src\models.txt', num_str3+1).strip(' ')
                                    new_line3 = new_line3.replace('\n', '')
                                    new_line3 = new_line3.strip(' ')
                                    # Определение названия модели и бренда и выход из вложенного цикла
                                    new_list3 = new_line3.split('\t')
                                    car_model_name = new_list3[1]
                                    brand = new_list3[2]
                                    break
                                else:
                                    h += 1

                        getcontext().prec = 8
                        price = Decimal(st[2])
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
                    j += 1
            i += 1
        model_dict_sorted = sorted(model_dict.items(), key=lambda item:item[1],  reverse=True)  # Сортировка
        top_models_by_sales = model_dict_sorted[0:3]   # Выбор первых трех в отсортированном списке
        first_model = f'{top_models_by_sales[0][0]}  {top_models_by_sales[0][1][2]}  {top_models_by_sales[0][1][0]}'
        second_model = f'{top_models_by_sales[1][0]}  {top_models_by_sales[1][1][2]}  {top_models_by_sales[1][1][0]}'
        third_model = f'{top_models_by_sales[2][0]}  {top_models_by_sales[2][1][2]}  {top_models_by_sales[2][1][0]}'
        ModelSaleStats = [first_model, second_model, third_model]
        return ModelSaleStats
