import json
import configparser
from user_VK import UserVK
from user_yandex import UserYandex


def copy_photo(vk_token, vk_user_id, ya_token, number_of_photos='5'):
    ## Выполнить резервное копирование фото из ВК на Яндекс.Диске
    vk = UserVK(vk_token, vk_user_id, number_of_photos)
    yandex = UserYandex(ya_token)
    vk.select_data_for_uploading()
    print(yandex.get_disk_info())
    yandex.uploading_photos_to_disk()


def create_info_file():
    list_info = {}
    with open('data_for_uploading.json') as f:
        name_size_list = json.load(f)
    count_photos = 0
    for key, value in name_size_list.items():
        count_photos += 1
        list_info[count_photos] = [{'file_name': key, 'size': value[1]}]
    with open('info_file.json', 'w', encoding='utf-8') as f:
        json.dump(list_info, f)
    return f'{count_photos} фото успешно загружены на Яндекс.Диск!'


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")
    access_token = config['VK']['vk_token']
    user = config['VK']['vk_user']
    yandex_token = config['Yandex']['yandex_token']
    # number_of_photos = '7'
    copy_photo(access_token, user, yandex_token)  # Добавить number_of_photos, если желаемое количество фото != 5
    print(create_info_file())
