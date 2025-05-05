from bs4 import BeautifulSoup
import requests as rq
import re, logging


def printable_degrees(dms):
    try:
        sign = dms[0]
        dms = dms[1:]  # Убираем знак для дальнейшей обработки

        # Определяем, сколько символов используется для градусов
        if len(dms) > 7:  # Если строка длиннее 7 символов, значит градусов - 3 символа
            degrees = (dms[:-7])
            minutes = (dms[-7:-5])
            seconds = (dms[-5:])
        else:  # Если строка короче или равна 7 символам, градусов - 2 символа
            degrees = (dms[:-6])
            minutes = (dms[-6:-4])
            seconds = (dms[-4:])
        return f"{sign}{degrees}°{minutes}'{seconds}\""
    except Exception as e:
        raise ValueError(f"Неверный формат входных данных: {dms}. Ошибка: {e}")


class IgsSite:
    def __init__(self, site_name=''):
        self.site_name = site_name
        self.base_log_url = "https://files.igs.org/pub/station/log/"
        self.log_url = self.get_log_link()
        self.deg_latitude, self.deg_longitude = '', ''
        self.dec_latitude, self.dec_longitude = 0.0, 0.0
        self.city_name = ''
        self.x, self.y, self.z = 0.0, 0.0, 0.0
        self.get_geo_cords()

    def __str__(self):
        return (f"IGS site:\t{self.city_name}:\tLATITUDE: {self.deg_latitude},\tLONGITUDE: {self.deg_longitude}\n"
                f"\t\tX: {self.x}, Y: {self.y}, Z: {self.z}")

    def get_log_link(self) -> str:
        logging.info("get_log_link")
        logging.info("Подключение к https://files.igs.org")
        response = rq.get(self.base_log_url)

        if response.status_code == 200:
            logging.info(f"Успешное подключение. Код ответа: {response.status_code}")

            soup = BeautifulSoup(response.text, "html.parser")
            regex = re.compile(re.escape(self.site_name), re.IGNORECASE)

            href = soup.find_all('a', string=regex)[0]['href']
            log_name = href.split('/')[-1]

            return self.base_log_url + log_name
        else:
            logging.error(f"Ошибка подключения. Код ответа: {response.status_code}")
            return ""

    def get_geo_cords(self):
        logging.info("get_geo_cords")
        logging.info(f"Подключение к {self.log_url}")
        response = rq.get(self.log_url)

        if response.status_code == 200:
            logging.info(f"Успешное подключение. Код ответа: {response.status_code}")

            logging.info("Парсинг журнала")
            log_text = response.text
            for line in log_text.split('\n'):
                if "Latitude" in line:
                    lat = re.search(r'[+-]\d+\.?\d+', line).group(0)
                    self.dec_latitude = lat
                    self.deg_latitude = printable_degrees(lat)
                if "Longitude" in line:
                    lon = re.search(r'[+-]\d+\.?\d+', line).group(0)
                    self.dec_longitude = lon
                    self.deg_longitude = printable_degrees(lon)
                if "City or Town" in line:
                    self.city_name = line.strip().split(':')[1][1:]
                if "X coordinate (m)" in line:
                    x = re.search(r'[+-]?\d+\.?\d+', line).group(0)
                    self.x = float(x)
                if "Y coordinate (m)" in line:
                    y = re.search(r'[+-]?\d+\.?\d+', line).group(0)
                    self.y = float(y)
                if "Z coordinate (m)" in line:
                    z = re.search(r'[+-]?\d+\.?\d+', line).group(0)
                    self.z = float(z)
        else:
            logging.error(f"Ошибка подключения. Код ответа: {response.status_code}")