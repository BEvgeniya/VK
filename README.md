# Публикация комиксов

Программа скачивает произвольный комикс с [xkcd.com](https://xkcd.com/) и публикует его в вашей группе ВКонтакте.

### Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, если есть конфликт с Python2) для установки зависимостей.

```bash
pip install -r requirements.txt
```
#### Переменные окружения:
- VK_ACCESS_TOKEN
- VK_GROUP_ID

Токен можно получить, следуя [инструкции](https://vk.com/dev/implicit_flow_user). Требуемые scopes: photos,groups,wall,offline. Group_id - id вашей группы ВКонтакте.

 
 ## Run

Запускается на Linux(Python 3) или Windows:

```bash

 python vk_comic.py

```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
