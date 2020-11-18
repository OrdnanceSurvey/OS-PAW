from os.path import normpath, join, dirname


# Additional Paths
repo_path = normpath(dirname(dirname(__file__)))
config_path = normpath(join(repo_path, 'config.ini'))


if __name__ == '__main__':
    print(config_path)