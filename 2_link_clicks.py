import os
import urllib.parse

import requests
from dotenv import load_dotenv


def shorten_link(token, url):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    api_version = '5.199'

    params = {
        'access_token': token,
        'v': api_version,
        'url': url
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    decoded_response = response.json()

    if 'error' in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response['error']['error_msg'])

    return decoded_response['response']['short_url']


def count_clicks(token, link):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    api_version = '5.199'
    key = urllib.parse.urlparse(link).path.lstrip('/')

    params = {
        'access_token': token,
        'v': api_version,
        'key': key,
        'interval': 'forever'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    decoded_response = response.json()

    if 'error' in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response['error']['error_msg'])

    stats = decoded_response['response']['stats']
    return sum(item['views'] for item in stats)


def is_shorten_link(token, url):
    url_parts = urllib.parse.urlparse(url)
    if url_parts.netloc != 'vk.cc':
        return False

    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    api_version = '5.199'
    key = url_parts.path.lstrip('/')

    params = {
        'access_token': token,
        'v': api_version,
        'key': key,
        'interval': 'forever'
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    decoded_response = response.json()

    return 'response' in decoded_response and 'error' not in decoded_response


def main():
    load_dotenv()

    try:
        vk_service_token = os.environ['VK_SERVICE_TOKEN']
    except KeyError:
        print('VK_SERVICE_TOKEN отсутствует')
        return

    user_input_url = input('Введите ссылку: ')

    try:
        if is_shorten_link(vk_service_token, user_input_url):
            total_clicks = count_clicks(vk_service_token, user_input_url)
            print('Кликов по ссылке:', total_clicks)
        else:
            short_url = shorten_link(vk_service_token, user_input_url)
            print('Сокращенная ссылка:', short_url)
    except (requests.exceptions.RequestException, KeyError) as error:
        print('Произошла ошибка:', error)


if __name__ == '__main__':
    main()