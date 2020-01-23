import sys
import getpass
import github

from . import create_database, save_repo_data


if sys.version_info < (3,):
    input = raw_input


def main(argv=None):
    filename ='insight_saver.db'

    create_database(filename)

    try:
        # Create an OAuth token by visiting https://github.com/settings/tokens
        # and generate a token with the scope: public_repo

        with open('token') as f:
            username = ''
            password = f.readline().strip()
            print('Using saved OAuth token')
    except FileNotFoundError:
        # Basic authentication method is deprecated

        print('Enter GitHub credentials')
        username = input('Username (or blank if using OAuth token): ')
        password = getpass.getpass('Password (or OAuth token): ')

    try:
        save_repo_data(username, password, filename)
    except github.BadCredentialsException:
        print('Unknown credentials, exiting.')
        sys.exit(1)
    except github.GithubException as e:
        print(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
