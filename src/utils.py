import os


def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'


def get_src_root():
    return os.path.dirname(os.path.abspath(__file__)) + '/'
