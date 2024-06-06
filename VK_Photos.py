import requests
from datetime import datetime
import json
from tqdm import tqdm


class UserVK:
    """   access_token = ''  - сюда необходимо вставить токен для ВК
          user_id = ''  - id пользователя ВК
          number_of_photos = '' - количество фото (если желаемое количество != 5 фото)
          (строки с переменными для ввода находятся в конце программы)
    """

    URL = 'https://api.vk.com/method/photos.get'

    def __init__(self, access_token, user_id, count_photos='5', version='5.236'):
        self.token = access_token
        self.id = user_id
        self.count = count_photos
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos_data(self):
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': True, 'count': self.count}
        response = requests.get(self.URL, params={**self.params, **params})
        data = response.json()['response']['items']
        return data

    def select_data_for_uploading(self):
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

    def create_info_file(self):
        list_info = {}
        with open('data_for_uploading.json') as f:
            name_size_list = json.load(f)
            count_photos = 0
        for key, value in name_size_list.items():
            count_photos += 1
            list_info[count_photos] = [{'file_name': key, 'size': value[1]}]
        with open('info_file.json', 'w', encoding='utf-8') as f:
            json.dump(list_info, f)
        return f'{self.count} фото готовы к загрузке'


class UserYandex:
    """   yandex_token = ''  - токен с Полигона Яндекс.Диска
          (строка с переменной для ввода находится в конце программы)
    """

    URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, yandex_token):
        self.token = yandex_token

    def create_a_folder(self):
        params = {'path': 'VK_photo'}
        headers = {'Authorization': self.token}
        response = requests.put(self.URL, params=params, headers=headers)
        return response.json()

    def uploading_photos_to_disk(self):
        folder = self.create_a_folder()
        with open('data_for_uploading.json') as f:
            data = json.load(f)
            list_data = list(data.items())
        for i in tqdm(range(len(list_data))):
            params = {'path': f'{folder["href"][-8:]}/{list_data[i][0]}', 'url': list_data[i][1][0]}
            headers = {'Authorization': self.token}
            response = requests.post(f'{self.URL}/upload', params=params, headers=headers)
        return 'Поздравляю! Ваши фото загружены на Яндекс.Диск!'



access_token = ''   # введите токен VK
user_id = ''   # введите id пользователя VK
yandex_token = ''   # введите токен с Полигона Яндекс.Диска
#  number_of_photos = ''
vk = UserVK(access_token, user_id)   # добавить number_of_photos, если желаемое количество фото != 5
yandex = UserYandex(yandex_token)
vk.select_data_for_uploading()
print(vk.create_info_file())
print(yandex.uploading_photos_to_disk())