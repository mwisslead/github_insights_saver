import sqlite3

from github import Github


def create_database(filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS views (id integer primary key, repository text, timestamp text, count integer, uniques integer, UNIQUE (repository, timestamp))''')
    c.execute('''CREATE TABLE IF NOT EXISTS clones (id integer primary key, repository text, timestamp text, count integer, uniques integer, UNIQUE (repository, timestamp))''')

    conn.commit()
    conn.close()


def save_repo_data(username, password, filename):
    session = Github(username, password)

    user = session.get_user()

    for repo in session.get_user().get_repos(affiliation='owner'):
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        for clone in repo.get_clones_traffic()['clones']:
            clone = clone.raw_data
            try:
                c.execute('''INSERT INTO clones (repository , timestamp, count, uniques) VALUES (?, ?, ?, ?)''', (repo.name, clone['timestamp'], clone['count'], clone['uniques']))
            except sqlite3.IntegrityError:
                c.execute('''UPDATE clones SET count = ?, uniques = ? where repository = ? and timestamp = ?''', (clone['count'], clone['uniques'], repo.name, clone['timestamp']))
                pass
        for view in repo.get_views_traffic()['views']:
            view = view.raw_data
            try:
                c.execute('''INSERT INTO views (repository , timestamp, count, uniques) VALUES (?, ?, ?, ?)''', (repo.name, view['timestamp'], view['count'], view['uniques']))
            except sqlite3.IntegrityError:
                c.execute('''UPDATE views SET count = ?, uniques = ? where repository = ? and timestamp = ?''', (view['count'], view['uniques'], repo.name, view['timestamp']))

        conn.commit()
        conn.close()
