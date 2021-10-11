from prettytable import PrettyTable

my_table = PrettyTable(field_names=[
    'stars',
    'forks_count',
    'issues',
    'url',
])


def leaderboard(forks_data, top_quantity=15):
    if forks_data.get('error'):
        print(f"An error has occurred: {forks_data['error']}")
    for i, repo in enumerate(sorted(forks_data['repositories'], key=lambda d: d['stars'], reverse=True)):
        my_table.add_row([
            repo['stars'],
            repo['forks_count'],
            repo['issues'],
            repo['url'],
        ])
        if i == top_quantity - 1:
            break
    print(my_table)
