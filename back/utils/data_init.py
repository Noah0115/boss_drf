import os
import pandas
import re
from tqdm import tqdm
import copy
import pickle
import numpy as np
import PIL.Image as Image
from wordcloud import WordCloud
import math
import unicodedata

"""CSV中skill、welfare字节处理"""

year = ["1-3", "3-5", "5-10", "经验不限", '在校']
education = ["中专", '大专', '本科', '硕士', '博士', "学历不限"]

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
def fullwidth_to_halfwidth(s):  # 全角转半角
    return ''.join([unicodedata.normalize('NFKC', char) for char in s])


def process_string(input_str):  # job_area转换
    if "·" in input_str:
        result_str = input_str.split("·")[0]
        return result_str
    else:
        return input_str


def newcsv():
    fieldnames = pandas.DataFrame(
        columns=['type', 'job_title', 'job_area', 'salary_bot', 'salary_top', 'year', 'education', 'company_title',
                 'company_info', 'skill',
                 'publis_name', 'welfare'])
    fieldnames['type'] = ''  # 职业名称
    fieldnames['job_title'] = ''  # 岗位名称
    fieldnames['job_area'] = ''  # 岗位地区
    fieldnames['salary_bot'] = 0  # 薪酬(低/月）
    fieldnames['salary_top'] = 0  # 薪酬(低/年）
    fieldnames['year'] = ''  # 经验情况
    fieldnames['education'] = ''  # 学历情况
    fieldnames['company_title'] = ''  # 公司名称
    fieldnames['company_info'] = ''  # 公司情况
    fieldnames['skill'] = ''  # 岗位技能
    fieldnames['publis_name'] = ''  # 招聘人
    fieldnames['welfare'] = ''  # 福利情况
    return fieldnames


# 获取所有职业文件
def getfiles():
    filenames = os.listdir("Job_csv")
    dataframe = newcsv()
    for filename in tqdm(filenames):
        x = pandas.read_csv("Job_csv/" + filename)
        job_edu = ''
        job_year = ''
        for i in range(len(x)):
            for y in year:
                if y in x['condition'][i]:  # 解析出经验数据
                    job_year = y
                    break
            for e in education:
                if e in x['condition'][i]:  # 解析出学历数据
                    job_edu = e
                    break
            money = re.findall(r'\d+', x['salary'][i])
            if '天' in x['salary'][i]:
                sala_bot = int(int(money[0]) * 365 / 12)
                sala_top = int(int(money[1]) * 365 / 12)
            else:
                sala_bot = int(money[0]) * 1000
                sala_top = int(money[1]) * 1000
            if len(money) > 2:
                sala_bot = int((sala_bot * int(money[2])) / 12)
                sala_top = int((sala_top * int(money[2])) / 12)
            s = {'type': x['type'][i],
                 'job_title': fullwidth_to_halfwidth(x['job_title'][i]),
                 'job_area': fullwidth_to_halfwidth(process_string(x['job_area'][i])),
                 'salary_bot': sala_bot,
                 'salary_top': sala_top,
                 'year': job_year,
                 'education': job_edu,
                 'company_title': x['company_title'][i],
                 'company_info': x['company_info'][i],
                 'skill': x['skill'][i],
                 'publis_name': x['publis_name'][i],
                 'welfare': x['welfare'][i]}
            # print(s)
            dataframe = dataframe._append([s], ignore_index=True)
    dataframe.to_csv('File/Boss_jobitem.csv', index=False)


# 对技能和福利数据进行处理
def select_skill():
    data = pandas.read_csv('File/Boss_jobitem.csv')
    job_dic = dict()

    for i in tqdm(range(len(data))):  # 分词处理
        type = data['type'][i]
        skill = re.split('[ 、]', str(data['skill'][i]))
        welfare = str(data['welfare'][i]).split('，')
        if type not in job_dic.keys():
            job_dic[type] = {'skill': [], 'welfare': []}
        job_dic[type]['skill'] += skill
        job_dic[type]['welfare'] += welfare
    sk = []
    we = []
    for t in job_dic.keys():  # 剔除包含词和大小写重复词
        skill = job_dic[t]['skill']
        welfare = job_dic[t]['welfare']
        for x in skill:
            if x == '':
                continue
            flag = True
            for i in range(len(sk)):
                y = sk[i]
                if x.upper() in y.upper():
                    flag = False
                    break
                elif y.upper() in x.upper():
                    flag = False
                    sk.pop(i)
                    sk.append(y)
                    break
            if flag:
                sk.append(x)
        for x in welfare:
            flag = True
            for i in range(len(we)):
                y = we[i]
                if x in y:
                    flag = False
                    break
                elif y in x:
                    flag = False
                    we.pop(i)
                    we.append(x)
                    break
            if flag:
                we.append(x)
    pickle.dump(job_dic, open('data/job_dic.pickle', 'wb'))  # 将字典写进pkl文件
    with open('File/skill.txt', "w", encoding='utf-8') as file:
        for x in sk:
            file.write(x + '\n')
    file.close()
    with open('File/welfare.txt', "w", encoding='utf-8') as file:
        for x in we:
            file.write(x + '\n')
    file.close()


# 计算全部职位分别有多少个岗位
def count_job():
    # 读取CSV文件
    data = pandas.read_csv('File/Boss_jobitem.csv')

    # 计算不同工作类型的数量
    job_counts = data['type'].value_counts()
    # 将结果按照指定格式输出
    result = {'all': [], **job_counts}
    pickle.dump(result, open('data/job_count.pickle', 'wb'))  # 将字典写进pkl文件


"""统计词语数目并计算出词语权重得分"""


def count_word():
    job_dic = pandas.read_pickle('data/job_dic.pickle')
    d_skill = []
    job_count = pandas.read_pickle('data/job_count.pickle')
    dic_count = dict()
    with open('File/skill.txt', "r", encoding='utf-8') as file:
        for x in file.readlines():
            d_skill.append([x.strip('\n'), 0])
    all_skill = copy.deepcopy(d_skill)  # 保存总体词语次数
    file.close()
    for job_name in tqdm(job_dic.keys()):
        sd = copy.deepcopy(d_skill)  # 保存当前职业中的词语次数
        for sk in job_dic[job_name]['skill']:
            for i in range(len(sd)):
                if sk.upper() in sd[i][0].upper():
                    sd[i][1] += 1
                    all_skill[i][1] += 1
                    break
        dic_count[job_name] = sd
    for job_name in tqdm(job_dic.keys()):
        sd = dic_count[job_name]
        for i in range(len(sd)):
            x = (sd[i][1] / job_count[job_name]) * (sd[i][1] / all_skill[i][1])
            sd[i][1] = int(x * 100)
        sd.sort(key=lambda x: x[1], reverse=True)
        fieldnames = pandas.DataFrame(columns=['skill', 'weight'])
        for x in sd:
            if x[1] >= 2:
                s = {'skill': x[0], 'weight': x[1]}
                fieldnames = fieldnames._append(s, ignore_index=True)
            else:
                break
        fieldnames.to_csv('weights/' + job_name + '.csv', index=False)


# 对福利信息进行统计处理
def count_weword():
    job_dic = pandas.read_pickle('data/job_dic.pickle')
    d_welfare = []
    with open('File/welfare.txt', "r", encoding='utf-8') as file:
        for x in file.readlines():
            d_welfare.append([x.strip('\n'), 0])
    file.close()
    for job_name in tqdm(job_dic.keys()):
        for sk in job_dic[job_name]['welfare']:
            for i in range(len(d_welfare)):
                if sk.upper() in d_welfare[i][0]:
                    d_welfare[i][1] += 1
                    break
        d_welfare.sort(key=lambda x: x[1], reverse=True)
        with open('data/welfare_count.txt', "w", encoding='utf-8') as file:
            for i in range(20):
                file.write(d_welfare[i][0] + '\n')


# 获得所有技能对应的权重得分
def getvector():
    filenames = os.listdir("weights")
    vector_weight = dict()
    vector = set()
    for file in filenames:
        data = pandas.read_csv("weights/" + file)
        file = file.strip('.csv')
        vector_weight[file] = dict()
        for i in range(len(data)):
            vector_weight[file][data['skill'][i]] = data['weight'][i]
            vector.add(data['skill'][i])
    with open('data/vector.txt', "w", encoding='utf-8') as file:
        for x in vector:
            file.write(x + '\n')
    file.close()
    pickle.dump(vector_weight, open('data/vector_weight.pickle', 'wb'))  # 将字典写进pkl文件


"""生成词云图"""


def getwordcloud():
    job_dic = pandas.read_pickle('data/job_dic.pickle')
    # mask_pic = np.array(Image.open("pic/1.jpg"))
    for job_name in tqdm(job_dic.keys()):
        space_word_list = ' '.join(job_dic[job_name]['skill'])
        word = WordCloud(
            font_path='C:/Windows/Fonts/simfang.ttf',  # 设置字体，本机的字体
            # mask=mask_pic,  # 设置背景图片
            background_color='white',  # 设置背景颜色
            max_font_size=150,  # 设置字体最大值
            max_words=2000,  # 设置最大显示字数
            stopwords={'的'}  # 设置停用词，停用词则不在词云途中表示
        ).generate(space_word_list)
        image = word.to_image()
        word.to_file('pic/' + job_name + '.png')  # 保存图片

def run():
    getfiles()
    select_skill()
    count_job()
    count_word()
    count_weword()
    getvector()
    return True
# getfiles()
# select_skill()
# count_job()
# count_word()
# count_weword()
