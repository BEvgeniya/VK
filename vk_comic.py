import os
import random

import requests


def load_comics(url, path):
    response = requests.get(url)
    response.raise_for_status()

    with open(path, 'wb') as file:
        return file.write(response.content)


def check_vk_api_response(response):
    response = response.json()
    try:
        error_text = response['error']['error_msg']
        error_code = response['error']['error_code']
        raise requests.HTTPError(f'Code: {error_code}. Error: {error_text}.')
    except KeyError:
        return


def upload_photo(path, server_url):
    with open(path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(server_url, files=files)
    response.raise_for_status()
    check_vk_api_response(response)
    response = response.json()
    photo = response['photo']
    photo_hash = response['hash']
    server = response['server']

    return photo, photo_hash, server


def get_wall_upload_server(access_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'v': '5.131',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    check_vk_api_response(response)
    upload_url = response.json()['response']['upload_url']
    return upload_url


def get_comic(filename, comic_random_number):
    url = f'https://xkcd.com/{comic_random_number}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    load_comics(comic['img'], filename)
    return comic['alt'], comic['title']


def save_photo(vk_group_id, vk_access_token, photo, photo_hash, server):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    params = {
        'group_id': vk_group_id,
        'access_token': vk_access_token,
        'v': '5.131',
        'photo': photo,
        'hash': photo_hash,
        'server': server

    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    check_vk_api_response(response)
    response = response.json()
    owner_id = response['response'][0]['owner_id']
    media_id = response['response'][0]['id']

    return owner_id, media_id


def post_photo(vk_access_token, vk_group_id, path, comic_comments, comic_title):

    server_url = get_wall_upload_server(vk_access_token, vk_group_id)
    photo, photo_hash, server = upload_photo(path, server_url)
    owner_id, media_id = save_photo(vk_group_id,
                                    vk_access_token,
                                    photo,
                                    photo_hash,
                                    server)

    url = 'https://api.vk.com/method/wall.post'
    params = {
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'attachments': f'photo{owner_id}_{media_id}',
        'message': f'{comic_title}. {comic_comments}',
        'access_token': vk_access_token,
        'v': '5.131',

    }

    response = requests.post(url, params=params)
    response.raise_for_status()
    check_vk_api_response(response)


def get_comic_random_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_count = response.json()['num']
    return random.randint(1, comics_count)


def main():
    path = 'comics_vk.png'

    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')

    comic_comments, comic_title = get_comic(path, get_comic_random_number())

    try:
        post_photo(vk_access_token, vk_group_id, path, comic_comments, comic_title)
    finally:
        os.remove(path)


if __name__ == '__main__':
    main()
