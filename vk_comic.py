import os
import random

import requests


def load_comics(url, path):
    response = requests.get(url)
    response.raise_for_status()

    with open(path, 'wb') as file:
        return file.write(response.content)


def upload_photo(path, server_url):
    with open(path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(server_url, files=files)
        response.raise_for_status()
        response = response.json()
        photo = response['photo']
        hash = response['hash']
        server = response['server']

    return [photo, hash, server]


def get_wall_upload_server(access_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'v': '5.131',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def get_comic():
    url = f'https://xkcd.com/{random.randint(1, 2529)}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    load_comics(comic['img'], 'comics_vk.png')
    return comic['alt'], comic['title']


def save_photo(vk_group_id, vk_access_token, path, upload_params):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    params = {
        'group_id': vk_group_id,
        'access_token': vk_access_token,
        'v': '5.131',
        'photo': upload_params[0],
        'hash': upload_params[1],
        'server': upload_params[2]

    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    response = response.json()
    owner_id = response['response'][0]['owner_id']
    media_id = response['response'][0]['id']

    return owner_id, media_id


def post_photo(vk_access_token, vk_group_id, path):
    comic_comments, comic_title = get_comic()

    server_url = get_wall_upload_server(vk_access_token, vk_group_id)
    upload_params = upload_photo(path, server_url)
    owner_id, media_id =\
    save_photo(vk_group_id, vk_access_token, path, upload_params)

    url = 'https://api.vk.com/method/wall.post'
    params = {
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': comic_title + '. ' + comic_comments,
        'access_token': vk_access_token,
        'v': '5.131',

    }

    response = requests.post(url, params=params)
    response.raise_for_status()


def main():
    path = 'comics_vk.png'

    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')

    try:
        post_photo(vk_access_token, vk_group_id, path)
    finally:
        os.remove(path)


if __name__ == '__main__':
    main()
