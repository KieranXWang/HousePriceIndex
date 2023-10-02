import os
import datetime


def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'


def get_src_root():
    return os.path.dirname(os.path.abspath(__file__)) + '/'


def convert_timestamp_to_readable_format(timestamp: int):
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    readable_format = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    return readable_format
