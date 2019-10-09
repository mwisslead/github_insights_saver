from setuptools import setup


def main():
    setup(
        name='github_insights_saver',
        version='0.0.0',
        packages=['github_insights_saver'],
        install_requires=['PyGithub'],
        entry_points = {
            'console_scripts': ['github_insights_saver=github_insights_saver.__main__:main'],
        }
    )


if __name__ == '__main__':
    main()
