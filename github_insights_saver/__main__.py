import sys
import getpass

from . import create_database, save_repo_data


def main(args):
    if args and args[0] == 'init':
        create_database()

    print('Enter github credentials')
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    save_repo_data(username, password)


if __name__ == '__main__':
    main(sys.argv[1:])
