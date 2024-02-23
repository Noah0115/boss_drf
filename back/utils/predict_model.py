"""模型预测"""
import os
import pandas
import re
from tqdm import tqdm
import copy
import pickle

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
class Score_model:
    def __init__(self):
        self.vector_weight=pandas.read_pickle('data/vector_weight.pickle')

    def count_score(self,skills):#计算技能点得分情况
        scores=[]
        for jobname in self.vector_weight.keys():
            vector=self.vector_weight[jobname]
            score=0
            for skill in skills:
                if skill in vector.keys():
                    score+=vector[skill]
            scores.append([jobname,score])
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def predict(self,skills):
        result=[]
        mix_scores=0
        scores=self.count_score(skills)
        for i in range(len(scores)):
            if i>=3 or scores[i][1]<=4:
                break
            result.append(scores[i])
            mix_scores+=scores[i][1]
        for i in range(len(result)):
            result[i][1]=str(int(result[i][1]/mix_scores*100))+"%"
        return result

def model_ceshi(skill):
    model=Score_model()
    # skill=['Vue','Django','全栈工程师','爬虫','运维经验','Nginx']
    result=model.predict(skill)
    print(result)
    return result
def model_test():
    model=Score_model()
    x=0
    y=0
    data=pandas.read_csv('File/Boss_jobitem.csv')
    for i in range(len(data)):
        result=model.predict(re.split('[ 、]',str(data['skill'][i])))
        print(result)
        if len(result)!=0:
            x+=1
            for xc in result:
                if xc[0]==data['Type'][i]:
                    y+=1
                    break
    print('权重阈值: 2')
    print('得分公式特征词权重  v1: 80%')
    print('得分公式学历权重  v2: 10%')
    print('得分公式经验权重  v3: 5%')
    print('得分公式其它因素权重  v4: 5%')
    print('当前模型的准确率为:'+str(y/x))
    return str(y/x)
# model_ceshi()