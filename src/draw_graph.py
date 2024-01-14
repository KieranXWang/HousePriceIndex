import matplotlib.pyplot as plt
import datetime

from src.utils import load_data_in_given_time_interval, convert_timestamp_to_readable_format


def generate_time_schedule_epoch(start_time: float, end_time: float, interval: float):
    schedule = []
    current = start_time

    while current < end_time:
        schedule.append(current)
        current = current + interval

    return schedule


def get_price_linear_interpolation(left_time_epoch: float, left_price: float, right_time_epoch: float,
                                   right_price: float, target_time_epoch: float):
    return left_price + (target_time_epoch - left_time_epoch) / (right_time_epoch - left_time_epoch) * (
            right_price - left_price)


def generate_index_list(records: list, start_time: datetime.datetime, end_time: datetime.datetime,
                        interval: datetime.timedelta):
    # generate time schedule
    start_timestamp = max(records[0]['timestamp'], start_time.timestamp())
    end_timestamp = min(records[-1]['timestamp'], end_time.timestamp())
    interval_seconds = interval.total_seconds()
    schedule = generate_time_schedule_epoch(start_time=start_timestamp, end_time=end_timestamp,
                                            interval=interval_seconds)

    # generate price data according to schedule
    price_schedule = [records[0]['price_data'], ]
    left = 0
    right = 1

    for i in range(1, len(schedule)):
        current_time = schedule[i]
        # find left and right so that current is in [left, right]
        while current_time >= records[right]['timestamp']:
            left += 1
            right += 1

        price_dict = {}

        # we get current price by linear interpolation using left and right
        for address in records[left]['price_data']:
            left_time = records[left]['timestamp']
            left_price = records[left]['price_data'][address]
            right_time = records[right]['timestamp']
            right_price = records[right]['price_data'].get(address, None)

            if not right_price:
                continue

            price = get_price_linear_interpolation(left_time, left_price, right_time, right_price, current_time)
            price_dict[address] = price

        # add price_dict to price schedule
        price_schedule.append(price_dict)

    # generate index data
    index_list = [1, ]
    for i in range(1, len(schedule)):
        index_factor_component = []
        price_data = price_schedule[i]

        for address in price_data:
            prev_price_data = price_schedule[i - 1]
            if address not in prev_price_data:
                continue
            factor = price_data[address] / prev_price_data[address]
            index_factor_component.append(factor)
        average_factor = sum(index_factor_component) / len(index_factor_component)
        index_val = index_list[i-1] * average_factor
        index_list.append(index_val)

    return schedule, index_list


def generate_graph_basic(schedule_list: list, index_list: list):
    # compute yearly change
    ##TODO: this is not correctly actually, improve yearly change conversion later
    yearly_change = (index_list[-1] - index_list[0]) / (schedule_list[-1] - schedule_list[0]) * datetime.timedelta(
        days=365).total_seconds()

    # create a figure and axis
    fig, ax = plt.subplots()

    x = list(range(len(schedule_list)))
    ax.plot(x, index_list, label=f'Index, yearly change = {yearly_change:.3f}')

    # set labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Index')

    # Replace x-axis ticks with strings
    x_tick_labels = [convert_timestamp_to_readable_format(ts, show_hours=False) for ts in schedule_list]
    ax.set_xticks(x)
    ax.set_xticklabels(x_tick_labels, rotation=90)

    # Add values of points to the graph
    for i, val in enumerate(index_list):
        txt = f"{val:.3f}"
        ax.text(x[i], index_list[i], f'{txt}', ha='right', va='bottom')

    # set title
    ax.set_title(f'House Price Index from {x_tick_labels[0]} to {x_tick_labels[-1]}')

    # legend
    ax.legend()

    return fig, ax


def plot(start_time: datetime.datetime, end_time: datetime.datetime, interval: datetime.timedelta, data_file_path: str,
         save_path: str):
    # load data
    records = load_data_in_given_time_interval(file_path=data_file_path, start_time=start_time, end_time=end_time)
    if len(records) < 2:
        raise ValueError("Does not have enough data points to draw the graph.")

    # generate index list
    schedule, index_list = generate_index_list(records=records, start_time=start_time, end_time=end_time,
                                               interval=interval)

    # draw graph
    fig, ax = generate_graph_basic(schedule_list=schedule, index_list=index_list)
    plt.tight_layout()
    fig.savefig(save_path)


if __name__ == '__main__':
    plot(start_time=datetime.datetime(year=2023, month=9, day=1),
         end_time=datetime.datetime(year=2024, month=1, day=10),
         interval=datetime.timedelta(days=10),
         data_file_path='/Users/kxw/Dropbox/HousePriceIndex/data/weekly/price_data.txt',
         save_path='./test_graph.png')
