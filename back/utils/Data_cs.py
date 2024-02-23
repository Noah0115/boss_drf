"""文本信息处理"""
import os
import pandas
import re
from tqdm import tqdm
import numpy as np
import copy
import pickle

# def getbriefly():
#     filenames=os.listdir("Job_conduct")
#     job_briefly=dict()
#
#     for filename in tqdm(filenames):
#         job_name=filename.strip('.txt')
#         job_briefly[job_name]=dict()
#         job_briefly[job_name]['introduce']=''
#         job_briefly[job_name]['content']=[]
#         with open('job_conduct/'+filename, "r",encoding='utf-8') as file:
#             describe=file.readlines()
#             for i in range(len(describe)):
#                 if i==0:
#                     job_briefly[job_name]['introduce']=describe[i].strip('\n')
#                 else:
#                     job_briefly[job_name]['content'].append(describe[i].strip('\n'))
#         file.close()
#     pickle.dump(job_briefly, open('data/job_briefly.pickle', 'wb'))  # 将字典写进pkl文件

#通过筛选进行职业推荐

def getcomjob(jobname,skill,education,welfare):
    data=pandas.read_csv('Job_csv/'+jobname+'_job_items.csv')
    result=[]
    for i in range(len(data)):
        dskill=data['skill'][i].upper()
        dwelfare=data['welfare'][i]
        deducation=data['condition'][i]
        if education in deducation or '经验不限' in deducation:
            se = 0
            we = 0
            for x in skill:
                if x.upper() in dskill:
                    se+=1
            for x in welfare:
                if x.upper() in dwelfare:
                    we+=1
            result.append([i,se,we])
    result.sort(key=lambda x: (x[1], x[2]), reverse=True)
    result=result[:10]
    st=[]
    for x in result:
        st.append(dict(data.loc[x[0]]))
    print(f"getcomjob返回结果:{st}")
    return st


getcomjob('java工程师',['Spring','Java','MySQL','后端开发'],'本科',['午餐补贴','零食下午茶','补充医疗保险','加班补助'])

# data=pandas.read_csv('Job_data/skill_type.csv', encoding='ANSI')
# skilltype=data.columns
# skills=[]
# for i in range(len(skilltype)):
#     oc=[]
#     sk=data[skilltype[i]]
#     for c in sk:
#         if c!= ' 1':
#             oc.append(c)
#         else:
#             break
#     skills.append({'ID': str(i), 'actsetid': str(i), 'act_addondesc': skilltype[i], 'act_addonvalue': oc,'selected':[]})
# for x in skills:
#     print(x)
# pickle.dump(skills, open('Job_data/data/skill_choice.pickle', 'wb'))  # 将字典写进pkl文件



