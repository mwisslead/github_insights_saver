import sys
import getpass
import github

from . import create_database, save_repo_data


if sys.version_info < (3,):
    input = raw_input


def main(argv=None):
    filename ='insight_saver.db'

    create_database(filename)

    print('Enter github credentials')
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    try:
        save_repo_data(username, password, filename)
    except github.BadCredentialsException:
        print('Unknown credentials, exiting.')
        sys.exit(1)


if __name__ == '__main__':
    main()
