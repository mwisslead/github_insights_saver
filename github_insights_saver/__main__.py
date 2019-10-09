import sys
import getpass

from . import create_database, save_repo_data


if sys.version_info < (3,):
    input = raw_input


def main(args):
    filename ='insight_saver.db'
    if args and args[0] == 'init':
        create_database(filename)

    print('Enter github credentials')
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    save_repo_data(username, password, filename)


if __name__ == '__main__':
    main(sys.argv[1:])
