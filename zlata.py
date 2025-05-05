import re
from math import acos, sqrt
from matplotlib import pyplot as plt
# Координаты опорной станции
xStation = 3898736.2
yStation = 855345.5
zStation = 4958372.6
# Номера выбранных спутников
satIds = [29, 26, 21]
# Классы для хранения данных
class Era:
    def __init__(self, data):
        self.hours = float(data[0])
        self.minutes = float(data[1])
        self.seconds = float(data[2])
        self.countSattelites = int(data[3])
        self.timeInSecs = self.hours * 3600 + self.minutes * 60 + self.seconds
        self.satellites = []

    def __str__(self):
        return str(self.timeInSecs)


class SatelliteData:
    def __init__(self, data):
        self.sat_id = int(data[0])
        self.x_sat = float(data[16])
        self.y_sat = float(data[17])
        self.z_sat = float(data[18])
# Чтение и обработка данных
eras = []
with open("data/leij_1-10.dat", 'r') as dataFile:
    dataFileLines = dataFile.readlines()
    tmpEra = None
    for line in dataFileLines:
        if '___Nsats' in line:
            parts = re.split(':|___Nsats:|\n', line)
            parts = [p for p in parts if p]
            if tmpEra:
                eras.append(tmpEra)
            tmpEra = Era(parts)
        else:
            parts = re.split(' |\t', line)
            parts = [p for p in parts if p]
            if tmpEra:
                tmpEra.satellites.append(SatelliteData(parts))
    if tmpEra:
        eras.append(tmpEra)
# Обработка и визуализация данных
for satId in satIds:
    w = []
    vLin = []
    rx, ry, rz, time = [0], [0], [0], [0]
    for era in eras:
        for sat in era.satellites:
            if sat.sat_id == satId:
                rx.append(sat.x_sat - xStation)
                ry.append(sat.y_sat - yStation)
                rz.append(sat.z_sat - zStation)
                time.append(era.timeInSecs)
                if len(time) > 2:
                    delta_time = time[-1] - time[-2]
                    if delta_time > 0:
                        dot_product = (rx[-1] * rx[-2] + ry[-1] * ry[-2] + rz[-1] * rz[-2])
                        magnitude1 = sqrt(rx[-2] ** 2 + ry[-2] ** 2 + rz[-2] ** 2)
                        print(magnitude1)
                        magnitude2 = sqrt(rx[-1] ** 2 + ry[-1] ** 2 + rz[-1] ** 2)
                        w.append(acos(dot_product / (magnitude1 * magnitude2)) / delta_time)
                        vLin.append(w[-1] * magnitude2 / 1000)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(time[2:], w)
    ax1.set_xlabel('Время, [с]')
    ax1.set_ylabel('Угловая скорость, [рад/c]')
    ax1.axhline(sum(w) / len(w), color='r', linestyle='--')
    ax2.plot(time[2:], vLin)
    ax2.set_xlabel('Время, [с]')
    ax2.set_ylabel('Линейная скорость, [км/c]')
    ax2.axhline(sum(vLin) / len(vLin), color='r', linestyle='--')
    fig.suptitle(f'Измерения для спутника {satId}')
    fig.savefig(f"figures/zlata/{satId}.png")