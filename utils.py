def get_fork_data(fork):
    return {
        'issues': fork['open_issues_count'],
        'stars': fork['stargazers_count'],
        'forks_count': fork['forks_count'],
        'url': fork['html_url']
    }
