from src.data_builder import DataBuilder
from src.utils import get_project_root


if __name__ == '__main__':
    root = get_project_root()
    data_builder = DataBuilder(price_database_path=root + 'data/weekly/price_data.txt')
    data_builder.run()



