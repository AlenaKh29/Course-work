from tqdm import tqdm
import requests
import json
import configparser


class UserYandex:

    URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.token = token

    def create_a_folder(self):
        #  Создать папку на Яндекс.Диске
        params = {'path': 'VK_photo'}
        headers = {'Authorization': self.token}
        response = requests.put(self.URL, params=params, headers=headers)
        return response.json()

    def uploading_photos_to_disk(self):
        # Прочитать json с данными файлов и загрузить на Яндекс.Диск.
        folder = self.create_a_folder()
        with open('data_for_uploading.json') as f:
            data = json.load(f)
        for key, value in tqdm(data.items()):
            params = {'path': f'{folder["href"][-8:]}/{key}', 'url': value[0]}
            headers = {'Authorization': self.token}
            requests.post(f'{self.URL}/upload', params=params, headers=headers)

    def get_disk_info(self):
        #  Получить информацию о корректном вводе токена.
        try:
            headers = {'Authorization': self.token}
            response = requests.get(self.URL[:-9], headers=headers)
            return f'Яндекс.Диск пользователя {response.json()["user"]["display_name"]}'
        except KeyError:
            return "Ошибка при вводе токена"


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")
    yandex_token = config['Yandex']['yandex_token']
    yandex = UserYandex(yandex_token)
    print(yandex.get_disk_info())
