import os
import pandas as pd
import os
import glob

def find_csv_files(directory):
    # 遍历目录及其所有子目录
    for root, dirs, files in os.walk(directory):
        # 对于每个子目录，查找 CSV 文件
        for file in glob.glob(os.path.join(root, '*.csv')):
            yield file


def utils_get_path_namelist(path):
    """
        工具函数：获取文件夹内文件全称
    :param path:
    :return:
    """
    # 使用os.listdir()获取文件夹下的所有文件和子文件夹的名称
    file_names = os.listdir(path)

    # 过滤出只是文件而不是子文件夹的名称
    file_names = [f for f in file_names if os.path.isfile(os.path.join(path, f))]
    file_names = sorted(file_names, key=lambda x: int(x.split('.')[0]))
    # 打印文件名列表
    print(f"{file_names}")
    return file_names


def utils_data_deduplicated_text(path_details, path_dedup_folder):
    """
        工具函数：语料去重,工具类,暂时不需要去重
    :return:
    """
    # path_details = "./data/coal_type/coal_type_data_details"
    # path_deduplicated = "./data/coal_type/coal_type_data_deduplicated"
    get_file_name_list = utils_get_path_namelist(path_details)
    for index, value in enumerate(get_file_name_list):
        with open(path_details + '/' + value) as f:
            sample_text_lines = f.read()
            df = pd.DataFrame({'text': sample_text_lines.split('\n')})
            df_deduplicated = df.drop_duplicates()
            deduplicated_text_pandas = '\n'.join(df_deduplicated['text'])
        with open(path_dedup_folder + f"\\dedup_{value}", "w", encoding="utf-8") as file:
            file.write(deduplicated_text_pandas)
            print(deduplicated_text_pandas)


def utils_ensure_folder_exists(folder_path):
    """
        工具函数：确保给定的文件夹路径存在。如果不存在，则创建它。
        参数：
        folder_path：要检查或创建的文件夹路径（字符串）。
        返回值：
        True：如果文件夹已经存在或成功创建。
        False：如果文件夹不能被创建。
        """
    if not os.path.isdir(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"文件夹 {folder_path} 已创建")
            return True
        except Exception as e:
            print(f"无法创建文件夹 {folder_path}，错误信息：{e}")
            return False
    else:
        print(f"文件夹 {folder_path} 已存在")
        return True


def check_file_exists(file_path):
    """
    检查指定文件是否存在。

    参数：
    file_path：要检查的文件的完整路径（字符串）。

    返回值：
    True：如果文件存在。
    False：如果文件不存在。
    """
    return os.path.isfile(file_path)
