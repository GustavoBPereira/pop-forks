import json
from time import time, sleep

import requests

from show_result import leaderboard
from utils import get_fork_data

GIT_HUB_API_URL = 'https://api.github.com'
exceeded_message = 'API rate limit exceeded'

main_repo_url = f'{GIT_HUB_API_URL}/repos/mattdiamond/Recorderjs'
main_repo_data = json.loads(requests.get(main_repo_url).text)
forks_url = [main_repo_data['forks_url']]


def get_forks_list(page=1, per_page=100):
    try:
        url = f'{forks_url[0]}?page={page}&per_page={per_page}'
    except IndexError:
        return []
    forks_request = requests.get(url, headers={'accept': 'application/vnd.github.v3+json'})
    if forks_request.status_code == 403:
        return exceeded_message
    return json.loads(forks_request.text)


fork_count = 0
page_number = 1
forks_data = {'repositories': []}

while forks_url:
    forks_lists = get_forks_list(page=page_number)

    if forks_lists == exceeded_message:
        forks_data['error'] = exceeded_message
        break
    if not forks_lists:
        if len(forks_url) > 0:
            page_number = 1
            forks_url.pop(0)

    for fork in forks_lists:
        data = get_fork_data(fork)
        forks_data['repositories'].append(data)

        if data['forks_count'] > 0:
            forks_url.append(fork['forks_url'])
        fork_count += 1

    page_number += 1
    sleep(0.5)

print(f'Quantidade de forks analizados: {fork_count}')

local_time_str = str(int(time()))
# int before call str to remove decimal numbers

with open(f'{local_time_str}.json', 'w', encoding='utf-8') as f:
    json.dump(forks_data, f, ensure_ascii=False, indent=4)

leaderboard(forks_data)
