import datetime as dt
import sqlite3
import requests

from github import Github


def create_database(filename):
    with sqlite3.connect(filename) as conn:
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS sync (id integer primary key, repository text, timestamp text, stars integer, watchers integer, forks integer, UNIQUE (repository, timestamp))''')
        for tbl in ['clones', 'views']:
            c.execute('''CREATE TABLE IF NOT EXISTS {} (id integer primary key, repository text, timestamp text, count integer, uniques integer, UNIQUE (repository, timestamp))'''.format(tbl))


def save_repo_data_raw(filename, repo, sync_dt):
    with sqlite3.connect(filename) as conn:
        c = conn.cursor()

        c.execute('''INSERT OR REPLACE INTO sync (repository , timestamp, stars, watchers, forks) VALUES (?, ?, ?, ?, ?)''', (repo.name, sync_dt, repo.stargazers_count, repo.subscribers_count, repo.forks_count))

        def update_table(tbl, d):
            c.execute('''INSERT OR REPLACE INTO {} (repository , timestamp, count, uniques) VALUES (?, ?, ?, ?)'''.format(tbl), (repo.name, d['timestamp'], d['count'], d['uniques']))

        for clone in repo.get_clones_traffic()['clones']:
            update_table('clones', clone.raw_data)

        for view in repo.get_views_traffic()['views']:
            update_table('views', view.raw_data)



def save_repo_data(username, password, filename, max_tries=5):
    session = Github(username, password)

    user = session.get_user()
    for j in range(max_tries):
        print('Gathering repositories{}'.format(' (attempt {}/{})'.format(j + 1, max_tries) if j > 0 else ''))

        try:
            filtered_repos = sorted([repo for repo in user.get_repos(affiliation='owner') if not repo.private], key=lambda x: x.name)
        except requests.ReadTimeout:
            if j == max_tries - 1:
                raise
            continue
        else:
            break

    sync_dt = dt.datetime.utcnow().isoformat() + 'Z'

    for i, repo in enumerate(filtered_repos):
        for j in range(max_tries):
            print('{}/{}: {}{}'.format(i + 1, len(filtered_repos), repo.html_url, ' (attempt {}/{})'.format(j + 1, max_tries) if j > 0 else ''))

            try:
                save_repo_data_raw(filename, repo, sync_dt)
            except requests.ReadTimeout:
                if j == max_tries - 1:
                    raise
                continue
            else:
                break
