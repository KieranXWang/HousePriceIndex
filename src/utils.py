import os
import datetime
import re

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'


def get_src_root():
    return os.path.dirname(os.path.abspath(__file__)) + '/'


def convert_timestamp_to_readable_format(timestamp: int):
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    readable_format = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    return readable_format


def parse_address(address: str):
    regex_pattern = r'(.*),\s?(\w+)\s(\w+)'
    try:
        m = re.match(regex_pattern, address)
        street_address = m.group(1)
        city = m.group(2)
        state = m.group(3)
    except Exception:
        raise ValueError(f'Failed to parse address: {address}')

    return street_address, city, state
