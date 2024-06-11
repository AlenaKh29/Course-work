import requests
from datetime import datetime
import json
import configparser


class UserVK:

    URL = 'https://api.vk.com/method/'

    def __init__(self, token, user, count_photos='5', version='5.199'):
        self.token = token
        self.id = user
        self.count = count_photos
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def check_id(self):
        #  Проверить, что используется: id или screen_name.
        if self.id.isdigit():
            result = self.id
        else:
            result = self.get_user_id()
        return result

    def get_user_id(self):
        #  Получить id, если используется screen_name.
        params = {'screen_name': self.id}
        response = requests.get(f'{self.URL}utils.resolveScreenName', params={**self.params, **params})
        user_id = response.json()
        return user_id['response']['object_id']

    def get_photos_data(self):
        # Получить данные файлов из ВК для дальнейшей обработки.
        try:
            params = {'owner_id': self.check_id(), 'album_id': 'profile', 'extended': True, 'count': self.count}
            response = requests.get(f'{self.URL}photos.get', params={**self.params, **params})
            data = response.json()['response']['items']
            return data
        except KeyError or TypeError:
            return 'Проверьте корректность введённых вами данных'

    def select_data_for_uploading(self):
        #  Выбрать и записать в json данные, необходимые для отправки файлов на облачный сервис.
        data = self.get_photos_data()
        url_for_uploading = {}
        list_likes = []
        for i in range(int(self.count)):
            photo_url = data[i]['sizes'][-1]['url']
            likes = data[i]["likes"]["count"]
            if likes not in list_likes:
                file_name = f'{likes}.jpeg'
                list_likes.append(likes)
            else:
                date = datetime.fromtimestamp(data[i]['date'])
                date_photo = str(date).split(' ')[0]
                file_name = f'{likes}_{date_photo}.jpeg'
            url_for_uploading[file_name] = [photo_url, data[i]['sizes'][-1]['type']]
        with open('data_for_uploading.json', 'w', encoding='utf-8') as f:
            json.dump(url_for_uploading, f)


if __name__ == '__main__':
    #  Проверка корректности введённых id или токена.
    config = configparser.ConfigParser()
    config.read("settings.ini")
    vk_id = config['VK']['vk_user']
    access_token = config['VK']['vk_token']
    vk = UserVK(access_token, vk_id)
    print(vk.get_photos_data())
