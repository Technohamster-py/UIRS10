from bs4 import BeautifulSoup
import requests as rq
import re, logging


class IgsSite:
    def __init__(self, site_name=''):
        self.site_name = site_name
        self.base_log_url = "https://files.igs.org/pub/station/log/"

    def get_log_link(self) -> str:
        logging.info("Подключение к https://files.igs.org")
        response = rq.get(self.base_log_url)

        if response.status_code == 200:
            logging.info(f"Успешное подключение! Код ответа: {response.status_code}")

            soup = BeautifulSoup(response.text, "html.parser")
            regex = re.compile(re.escape(self.site_name), re.IGNORECASE)

            href = soup.find_all('a', string=regex)[0]['href']
            log_name = href.split('/')[-1]

            return self.base_log_url + log_name
        else:
            logging.error(f"Ошибка подключения. Код ответа: {response.status_code}")
            return ""

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    igs = IgsSite('leij')
    print(igs.get_log_link())