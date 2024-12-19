from datetime import datetime, timedelta

import requests

def get_vacancies(count=10, name_filter=''):
    keys = ['name', 'employer', 'area', 'salary', 'published_at', 'created_at']
    date_from = (datetime.now() - timedelta(hours=10)).isoformat() + 'Z'
    params = {
                'date_from': date_from,
                'text': name_filter,
                'per_page': count,
                'page': 0
            }
    response = requests.get('https://api.hh.ru/vacancies', params=params)
    data = response.json()['items']
    result = {}
    for item in data:
        info_list = {}
        for key in keys:
            if key == 'area' or key == 'employer':
                info_list[key] = item[key]['name']
            elif key == 'salary' and item[key] is None:
                info_list[key] = 'Зарплата не указана'
            elif key == 'salary' and item[key]['to'] is None:
                info_list[key] = f'От {item[key]["from"]} ({item[key]["currency"]})'
            elif key == 'salary' and item[key]['from'] is None:
                info_list[key] = f'До {item[key]["to"]} ({item[key]["currency"]})'
            elif key == 'salary' and item[key]:
                info_list[key] = f'От {item[key]["from"]} до {item[key]["to"]} ({item[key]["currency"]})'
            else:
                info_list[key] = item[key]
        result[item['id']] = info_list
    return result
print(get_vacancies().items())