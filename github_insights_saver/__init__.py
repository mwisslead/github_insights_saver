import datetime as dt
import sqlite3

from github import Github


def create_database(filename):
    with sqlite3.connect(filename) as conn:
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS views (id integer primary key, repository text, timestamp text, count integer, uniques integer, UNIQUE (repository, timestamp))''')
        c.execute('''CREATE TABLE IF NOT EXISTS clones (id integer primary key, repository text, timestamp text, count integer, uniques integer, UNIQUE (repository, timestamp))''')
        c.execute('''CREATE TABLE IF NOT EXISTS sync (id integer primary key, repository text, timestamp text, stars integer, watchers integer, forks integer, UNIQUE (repository, timestamp))''')


def save_repo_data(username, password, filename):
    session = Github(username, password)

    user = session.get_user()

    timestamp = dt.datetime.utcnow().isoformat() + 'Z'
    filtered_repos = sorted([repo for repo in user.get_repos(affiliation='owner') if not repo.private], key=lambda x: x.name)
    for i, repo in enumerate(filtered_repos):
        print('{}/{}: {}'.format(i+1, len(filtered_repos), repo.html_url))
        with sqlite3.connect(filename) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO sync (repository , timestamp, stars, watchers, forks) VALUES (?, ?, ?, ?, ?)''', (repo.name, timestamp, repo.stargazers_count, repo.subscribers_count, repo.forks_count))
            for clone in repo.get_clones_traffic()['clones']:
                clone = clone.raw_data
                try:
                    c.execute('''INSERT INTO clones (repository , timestamp, count, uniques) VALUES (?, ?, ?, ?)''', (repo.name, clone['timestamp'], clone['count'], clone['uniques']))
                except sqlite3.IntegrityError:
                    c.execute('''UPDATE clones SET count = ?, uniques = ? where repository = ? and timestamp = ?''', (clone['count'], clone['uniques'], repo.name, clone['timestamp']))
            for view in repo.get_views_traffic()['views']:
                view = view.raw_data
                try:
                    c.execute('''INSERT INTO views (repository , timestamp, count, uniques) VALUES (?, ?, ?, ?)''', (repo.name, view['timestamp'], view['count'], view['uniques']))
                except sqlite3.IntegrityError:
                    c.execute('''UPDATE views SET count = ?, uniques = ? where repository = ? and timestamp = ?''', (view['count'], view['uniques'], repo.name, view['timestamp']))
