import json
import os.path
import time
import csv
import warnings
from tqdm import tqdm

from src.utils import get_project_root, convert_timestamp_to_readable_format
from src.redfin_utils import get_current_price


root = get_project_root()


class DataBuilder:
    def __init__(self, realty_database_path: str = root + 'realty_database/seattle.csv',
                 price_database_path: str = root + 'data/weekly/price_data.txt',
                 latest_update_path: str = ''):
        # timestamp
        self.timestamp = int(time.time())  # 10-digit epoch time

        # settings
        self.realty_database_path = realty_database_path
        self.price_database_path = price_database_path
        self.latest_update_path = latest_update_path

        # address to fetch price data for
        self.address_list = self.load_realty_address()
        self.price_dict = {address: None for address in self.address_list}

    def load_realty_address(self) -> list:
        with open(self.realty_database_path, mode='r') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)
            # skip header
            next(csv_reader)
            address_list = [row[0] for row in csv_reader]

        return address_list

    def request_price_data(self):
        print('Requesting price data ...')
        with tqdm(total=len(self.address_list), desc="Processing") as pbar:
            for address in self.price_dict:
                try:
                    price = int(get_current_price(address))
                    self.price_dict[address] = price
                except Exception as e:
                    warnings.warn(f"Unable to fetch price data for {address}: {str(e)}")
                pbar.update(1)

    def save_price_data(self):
        print('Saving price data ...')
        data = {'timestamp': self.timestamp, 'price_data': self.price_dict}
        data_json = json.dumps(data)
        if os.path.exists(self.price_database_path):
            with open(self.price_database_path, 'a', encoding='utf-8') as f:
                f.write(data_json)
                f.write('\n')
        else:
            with open(self.price_database_path, 'w', encoding='utf-8') as f:
                f.write(data_json)
                f.write('\n')

    def update_lastest_update_file(self):
        with open(self.latest_update_path, 'w+', encoding='utf-8') as f:
            f.write('lastest update:\n')
            f.write(convert_timestamp_to_readable_format(self.timestamp))

    def run(self):
        self.request_price_data()
        self.save_price_data()
        if self.latest_update_path:
            self.update_lastest_update_file()


if __name__ == '__main__':
    data_builder = DataBuilder(price_database_path=root + 'data/test/test_build.txt')
    data_builder.run()


