import json
import sys
from time import sleep

import requests

from show_result import leaderboard
from utils import get_fork_data, get_api_url_by_repository_url, create_json

exceeded_message = 'API rate limit exceeded'


def get_forks_list(forks_url, page=1, per_page=100):
    try:
        url = f'{forks_url[0]}?page={page}&per_page={per_page}'
    except IndexError:
        return []
    forks_request = requests.get(url, headers={'accept': 'application/vnd.github.v3+json'})
    if forks_request.status_code == 403:
        return exceeded_message
    return json.loads(forks_request.text)


def crawl_forks(forks_api_url):
    fork_count = 0
    page_number = 1
    forks_data = {'repositories': []}
    forks_url = [forks_api_url]

    while forks_url:
        forks_lists = get_forks_list(forks_url, page=page_number)

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

    print(f'Number of analyzed forks: {fork_count}')
    return forks_data


if __name__ == '__main__':
    # First parameter (sys.argv[1]) = github repository url
    try:
        repository_url = get_api_url_by_repository_url(sys.argv[1])
    except IndexError as err:
        raise Exception('Github repository url is required in the first parameter') from err

    try:
        top_quantity = int(sys.argv[2])
    except IndexError:
        top_quantity = 15
    except ValueError as err:
        raise Exception('Top quantity must be an integer value') from err

    main_repo_data = json.loads(requests.get(repository_url).text)

    forks_data = crawl_forks(main_repo_data['forks_url'])

    create_json(forks_data)
    leaderboard(forks_data, top_quantity)
