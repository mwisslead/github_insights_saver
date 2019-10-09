# github insights saver
Save github repository stats to a sqlite3 database to allow longer than 14 days of insights data


## Installation
`python setup.py install`

## Usage
```
    $ github_insights_saver
```

To start using simply install and run the command `github_insights_saver` or `python -m github_insights_saver`. After running, data will be stored to the sqlite3 database file `insights_saver.db`. Running again in the same directory will update the database.
