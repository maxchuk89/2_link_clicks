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
    response_data = response.json()

    return response_data['response']['short_url']


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
    response_data = response.json()
    stats = response_data['response']['stats']

    return sum(item['views'] for item in stats)


def is_shorten_link(token, url):
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc != 'vk.cc':
        return False


    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    api_version = '5.199'
    key = parsed.path.lstrip('/')

    params = {
        'access_token': token,
        'v': api_version,
        'key': key,
        'interval': 'forever'
    }

    response = requests.get(api_url, params=params)
    response_data = response.json()

    return 'response' in response_data


def main():
    load_dotenv()

    token = os.getenv('API_KEY')
    url = input('Введите ссылку: ')

    try:
        if is_shorten_link(token, url):
            clicks = count_clicks(token, url)
            print('Кликов по ссылке:', clicks)
        else:
            short_url = shorten_link(token, url)
            print('Сокращенная ссылка:', short_url)
    except Exception as error:
        print('Произошла ошибка:', error)


if __name__ == '__main__':
    main()