import json
from time import time

GIT_HUB_API_URL = 'https://api.github.com'


def get_fork_data(fork):
    return {
        'issues': fork['open_issues_count'],
        'stars': fork['stargazers_count'],
        'forks_count': fork['forks_count'],
        'url': fork['html_url']
    }


def get_api_url_by_repository_url(url):
    splited_url = url.split('/')
    user, repo_name = splited_url[-2], splited_url[-1]
    return f'{GIT_HUB_API_URL}/repos/{user}/{repo_name}'


def create_json(data):
    local_time_str = str(int(time()))
    # int before call str to remove decimal numbers

    with open(f'{local_time_str}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
