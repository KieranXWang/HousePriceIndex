import os
import datetime
import re
import json
import bisect


def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'


def get_src_root():
    return os.path.dirname(os.path.abspath(__file__)) + '/'


def convert_timestamp_to_readable_format(timestamp: float, show_hours: bool = True):
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    if show_hours:
        readable_format = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        readable_format = datetime_obj.strftime('%Y-%m-%d')
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


def binary_search_find_interval(arr: list, target: float):
    right_index = bisect.bisect_left(arr, target)

    if right_index >= len(arr):
        return right_index - 1, right_index
    elif arr[right_index] > target:
        return right_index - 1, right_index
    else:
        return right_index, right_index


def load_data_file_txt(file_path: str):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        records = [json.loads(line) for line in lines]

    return records


def load_data_in_given_time_interval(file_path: str, start_time: datetime.datetime, end_time: datetime.datetime,
                                     one_more_at_end: bool = True, one_more_at_front: bool = True):
    records = load_data_file_txt(file_path)

    start_timestamp = start_time.timestamp()
    end_timestamp = end_time.timestamp()

    # find where start_time and end_time lie in
    record_ts_list = [record['timestamp'] for record in records]
    start_left_index, start_right_index = binary_search_find_interval(record_ts_list, start_timestamp)
    end_left_index, end_right_index = binary_search_find_interval(record_ts_list, end_timestamp)

    if start_left_index < 0:
        # start timestamp is out of boundary, record start point is 0
        start_point = 0
    else:
        # depends on if we want one more at front
        if one_more_at_front:
            start_point = start_left_index
        else:
            start_point = start_right_index

    if end_right_index >= len(record_ts_list):
        # end timestamp is out of boundary, record ends at last
        end_point = end_left_index
    else:
        # depends on if we want one more at end
        if one_more_at_end:
            end_point = end_right_index
        else:
            end_point = end_left_index

    return records[start_point:end_point+1]


def convert_to_yearly_rate(rate: float, period: datetime.timedelta):
    days = period.total_seconds() / 60 / 60 / 24
    yearly_rate = (rate ** (1 / days)) ** 365
    return yearly_rate

