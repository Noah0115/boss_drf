from sqlalchemy import create_engine
import os
from back.utils.Tools import find_csv_files
import pandas as pd
# 数据库连接信息（根据你的数据库信息进行替换）
username = 'root'
password = '123456'
host = '127.0.0.1'
database = 'boss_drf'
port = '3306'

# 创建数据库连接
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}', echo=True)

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
def single_data_import(csv_path,table_name):
    """
    将单个CSV导入数据库中
    :param csv_path:CSV文件路径
    :param table_name:导入的表名
    :return:
    """
    csv = pd.read_csv(csv_path)
    # 为数据添加 'status' 列，其值为 1
    # csv['status'] = 1
    # 将数据导入到 MySQL 数据库中（假设表名为 your_table）
    csv.to_sql(table_name, con=engine, if_exists='append', index=False)



def all_csv_conbine():
    """
    将目录下所有CSV合并为一个CSV文件
    :return:
    """
    # 定义一个空的 DataFrame 用于存储合并后的数据
    combined_csv = pd.DataFrame()
    food_data_path_prefix = "./data"
    csv_files = find_csv_files(food_data_path_prefix)

    # 使用列表推导式读取所有文件
    dfs = [pd.read_csv(file.replace('\\', '/')) for file in csv_files]

    # 使用 pd.concat() 合并所有 DataFrame
    combined_csv = pd.concat(dfs, ignore_index=True)

    # 保存合并后的 CSV 文件
    combined_csv.to_csv("combined_csv.csv", index=False)

def all_data_import():
    """
    将目录下所有CSV文件导入到MYSQL中
    :return:
    """
    food_data_path_prefix = "./File"
    food_data_table = 'back_jobinfo'
    csv_files = find_csv_files(food_data_path_prefix)
    for file in csv_files:
        single_data_import(file.replace('\\', '/'),food_data_table)
    # single_data_import('all_types.csv',food_types_table)

def run_sql():
    all_data_import()   # 目录下CSV文件导入数据库中
if __name__ == '__main__':
    all_data_import()   # 目录下CSV文件导入数据库中
    # all_csv_conbine()   # 目录下所有CSV合并至一个CSV中