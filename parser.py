import pprint
from datetime import timedelta
import csv
import logging


class DataParser:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = self.parse_to_sat_dict()

    def convert_to_csv(self) -> str:
        logging.info(f'Converting {self.filename} to csv')
        input_data = self.parse_to_string_dict()
        # Все из задания
        fieldnames = ['epoch',              # Эпоха (Ч:ММ:С)
                      'satid',              # номер спутника
                      'ro',                 # скорректированная дальность до спутника с учётом ряда смещений в измерениях
                      'P1',                 # измерение псевдодальности на частоте L1 (метры)
                      'P2',                 # измерение псевдодальности на частоте L2 (метры)
                      'L1',                 # измерение псевдофазы на частоте L1 (метры)
                      'L2',                 # измерение псевдофазы на частоте L2 (метры)
                      'Mw',                 # функция отображения для влажной составляющей тропосферной задержки (б/р)
                      'Md',                 # функция отображения для сухой составляющей тропосферной задержки (б/р)
                      'Td',                 # расчётная сухая составляющая тропосферной задержки (метры)
                      'Tw',                 # расчётная влажная составляющая тропосферной задержки (метры)
                      'Tw_estimate',        # -
                      'dt',                 # смещение показаний спутниковых часов относительно показаний часов системы (метры)
                      'dTrec_estimate',     # меньше знаешь, крепче спишь (метры)
                      'A',                  # действительное значение неоднозначности псевдофазового измерения (метры)
                      'windup_metr',        # wind-up поправка (метры)
                      'elevation',          # угол возвышения (градусы)
                      'x_sat',              # X координата спутника на момент предшествия (метры)
                      'y_sat',              # Y координата спутника на момент предшествия (метры)
                      'z_sat',              # Z координата спутника на момент предшествия (метры)
                      'P3',                 # ионосферосвободная комбинация измерений псевдодальности P1 и P2 (метры)
                      'L3',                 # ионосферосвободная комбинация измерений псевдофазы L1 и L2 (метры)
                      'R_geom'              # геометрическая дальность до спутника (метры)
                      ]
        csv_filename = self.filename.split('.')[0] + '.csv' # формируем имя файла csv

        # Открываем файл csv и записываем в него табличку
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader() # записываем заголовки (из задания)
            for epoch in input_data.keys(): # проходимся по эпохам
                for sat in input_data[epoch]: # проходимся по спутникам внутри эпохи
                    sat['epoch'] = epoch    # Записываем значение эпохи в данные о спутнике
                    writer.writerow(sat)    # Записываем данные о спутнике в файл (одна строчка)
        return csv_filename

    def epoch_to_sat_dict(self) -> dict:
        """
        Конвертируем словарь {эпоха : SatVision} в словарь {спутник : SatVision}
        :return:
        """
        logging.info(f'Converting {self.filename} to sat dict')
        sat_data = {}
        for epoch in self.data.keys():
            for satellite in self.data[epoch]:
                if not satellite.satid in sat_data.keys():
                    sat_data[satellite.satid] = [satellite]
                else:
                    sat_data[satellite.satid].append(satellite)
        return sat_data

    def parse_to_string_dict(self) -> dict:
        """
        Парсим исходный файл в словарь {эпоха: данные спутников в эту эпоху (тоже словарь)}
        :return:
        """
        logging.info(f'Parsing {self.filename} to string dict')
        current_epoch = ""
        data = {}
        with open(self.filename, 'r') as f:
            for line in f:
                if not line.startswith('   '):
                    epoch = line.strip().split('.')[0].split(':')
                    current_epoch = float(epoch[0]) * 3600 + float(epoch[1]) * 60 + float(epoch[2])
                    data[current_epoch] = []
                else:
                    line = line.strip()
                    sat = {}
                    sat['satid'], sat['ro'], sat['P1'], sat['P2'], sat['L1'], sat['L2'], sat['Mw'], sat['Md'], sat[
                        'Td'], sat['Tw'], sat['Tw_estimate'], sat['dt'], sat['dTrec_estimate'], sat['A'], sat[
                        'windup_metr'], sat['elevation'], sat['x_sat'], sat['y_sat'], sat['z_sat'], sat['P3'], sat[
                        'L3'], sat['R_geom'] = tuple(line.split('\t'))
                    data[current_epoch].append(sat)
        return data

    def parse_to_sat_dict(self) -> dict:
        """
        Парсим исходный файл в словарь {эпоха: данные спутников в эту эпоху (Класс SatVision)}
        :return:
        """
        logging.info(f'Parsing {self.filename} to sat dict') # Отправляем сообщение в лог
        current_epoch = ""
        data = {}   # Делаем заготовки данных
        with open(self.filename, 'r') as f:
            for line in f:  # Перебираем исходный файл по строчкам
                if not line.startswith('   '):  # Находим строчку, в которой записана эпоха
                    current_epoch = self.parse_time(line.strip().split('.')[0])
                    data[current_epoch] = []    # Делаем заготовку данных внутри эпохи
                else:
                    line = line.strip()
                    sat = {}
                    sat['satid'], sat['ro'], sat['P1'], sat['P2'], sat['L1'], sat['L2'], sat['Mw'], sat['Md'], sat[
                        'Td'], sat['Tw'], sat['Tw_estimate'], sat['dt'], sat['dTrec_estimate'], sat['A'], sat[
                        'windup_metr'], sat['elevation'], sat['x_sat'], sat['y_sat'], sat['z_sat'], sat['P3'], sat[
                        'L3'], sat['R_geom'] = tuple(line.split('\t'))  # Собираем данные по спутнику в словарь
                    vision = SatVision(sat, current_epoch)  # Создаем элемент класса SatVision
                    data[current_epoch].append(vision)  # Добавляем его в список спутников в конкретную эпоху
        return data

    def parse_time(self, time_str) -> timedelta:
        """
        парсим строчку времени в формат timedelta
        :param time_str:
        :return:
        """
        h, m, s = tuple(map(int, time_str.split(':')))
        return timedelta(hours=h, minutes=m, seconds=s)


class SatVision:
    def __init__(self, sat_params, epoch):
        self.epoch = epoch
        self.satid = sat_params['satid']
        self.ro = float(sat_params['ro'])
        self.P1 = float(sat_params['P1'])
        self.P2 = float(sat_params['P2'])
        self.L1 = float(sat_params['L1'])
        self.L2 = float(sat_params['L2'])
        self.Mw = float(sat_params['Mw'])
        self.Md = float(sat_params['Md'])
        self.Td = float(sat_params['Td'])
        self.Tw = float(sat_params['Tw'])
        self.Tw_estimate = float(sat_params['Tw_estimate'])
        self.dt = float(sat_params['dt'])
        self.dTrec_estimate = float(sat_params['dTrec_estimate'])
        self.A = float(sat_params['A'])
        self.windup_metr = float(sat_params['windup_metr'])
        self.elevation = float(sat_params['elevation'])
        self.x_sat = float(sat_params['x_sat'])
        self.y_sat = float(sat_params['y_sat'])
        self.z_sat = float(sat_params['z_sat'])
        self.P3 = float(sat_params['P3'])
        self.L3 = float(sat_params['L3'])
        self.R_geom = float(sat_params['R_geom'])

    def __str__(self):
        return f"{self.satid=}\t{self.epoch}"