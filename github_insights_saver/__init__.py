import datetime as dt
import sqlite3

from github import Github


def create_database(filename):
    with sqlite3.connect(filename) as conn:
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS sync (id integer primary key, repository text, timestamp text, stars integer, watchers integer, forks integer, UNIQUE (repository, timestamp))''')
        for tbl in ['clones', 'views']:
            c.execute('''CREATE TABLE IF NOT EXISTS {} (id integer primary key, repository text, timestamp text, count integer, uniques integer, UNIQUE (repository, timestamp))'''.format(tbl))


def save_repo_data(username, password, filename):
    session = Github(username, password)

    user = session.get_user()
    filtered_repos = sorted([repo for repo in user.get_repos(affiliation='owner') if not repo.private], key=lambda x: x.name)

    sync_dt = dt.datetime.utcnow().isoformat() + 'Z'

    for i, repo in enumerate(filtered_repos):
        print('{}/{}: {}'.format(i+1, len(filtered_repos), repo.html_url))

        with sqlite3.connect(filename) as conn:
            c = conn.cursor()

            c.execute('''INSERT INTO sync (repository , timestamp, stars, watchers, forks) VALUES (?, ?, ?, ?, ?)''', (repo.name, sync_dt, repo.stargazers_count, repo.subscribers_count, repo.forks_count))

            def update_table(tbl, d):
                try:
                    c.execute('''INSERT INTO {} (repository , timestamp, count, uniques) VALUES (?, ?, ?, ?)'''.format(tbl), (repo.name, d['timestamp'], d['count'], d['uniques']))
                except sqlite3.IntegrityError:
                    c.execute('''UPDATE {} SET count = ?, uniques = ? where repository = ? and timestamp = ?'''.format(tbl), (d['count'], d['uniques'], repo.name, d['timestamp']))

            for clone in list(repo.get_clones_traffic()['clones']):
                update_table('clones', clone.raw_data)

            for view in list(repo.get_views_traffic()['views']):
                update_table('views', view.raw_data)
