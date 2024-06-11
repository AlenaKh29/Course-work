#### Перед запуском программы в файле <u>_settings.ini_</u> необходимо ввести данные:

vk_token = ...***токен ВК***...

vk_user = ...***id*** или ***screen name*** пользователя ВК...

yandex_token = ...***токен с Полигона Яндекс.Диска***...

___
#### Следуя вашим замечаниям после первой проверки работы, внесла изменения:
1. Пользователь может ввести как id, так и screen_name.
2. Функция, сохраняющая json-файл с информацией о фото, теперь не зависит от класса UserVK.
3. Классы UserVK и UserYandex вынесены в отдельные модули, также добавлена обработка исключений при некорректном вводе токенов, id или screen_name.
4. Из глобального всё убрано.
5. Токены и id теперь читаются из файла "settings.ini", куда их необходимо сначала внести(надеюсь, я правильно поняла логику)

