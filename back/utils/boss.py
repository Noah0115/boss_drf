import os
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from lxml import etree
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def newcsv():
    fieldnames = pd.DataFrame(
        columns=['type', 'job_title', 'job_area', 'salary', 'condition', 'company_title', 'company_info', 'skill',
                 'publis_name', 'welfare'], dtype='str')
    fieldnames['type'] = ''  # 职业名称
    fieldnames['job_title'] = ''  # 岗位名称
    fieldnames['job_area'] = ''  # 岗位地区
    fieldnames['salary'] = ''  # 薪酬
    fieldnames['condition'] = ''  # 岗位情况
    fieldnames['company_title'] = ''  # 公司名称
    fieldnames['company_info'] = ''  # 公司情况
    fieldnames['skill'] = ''  # 岗位技能
    fieldnames['publis_name'] = ''  # 招聘人
    fieldnames['welfare'] = ''  # 福利情况
    return fieldnames

class Boss(object):
    def __init__(self):
        self.data_list = list()  # 数据列表

    def screen_size(self):
        """使用tkinter获取屏幕大小"""
        import tkinter  # GUI工具库
        tk = tkinter.Tk()  # 创建窗口
        width = tk.winfo_screenwidth()  # 获取屏幕宽度
        height = tk.winfo_screenheight()  # 获取屏幕高度
        tk.quit()  # 关闭窗口
        return width, height  # 返回屏幕宽度和高度

    def input_time_random(self):
        return random.randint(100, 151)  # 生成随机的输入延迟时间

    def main(self, jobname, filename, df):
        options = Options()
        # 指定用户数据目录的路径
        current_directory = os.path.dirname(os.path.abspath(__file__))
        user_data_dir = "/config"
        options.add_argument(f"user-data-dir={current_directory+user_data_dir}")
        # options.headless = True  # 无头模式
        driver = webdriver.Chrome(options=options)
        # 这里调用 parse_html 作为生成器
        # driver.get('https://www.zhipin.com/?city=100010000&ka=city-sites-100010000')
        i = 1
        flag = True
        while flag:
            print(i, '页', filename)
            driver.get(f'https://www.zhipin.com/web/geek/job?query={jobname}&city=100010000&page={i}')
            # 检查是否出现了验证页面
            time.sleep(7)
            if 'verify-slider' in driver.current_url:
                print("检测到验证页面，等待手动验证...")

                # 等待手动验证，可以通过检测URL变化或其他方式
                while 'verify-slider' in driver.current_url:
                    time.sleep(5)  # 简单地等待1秒再次检查
                print("验证完成，继续执行程序。")
                driver.get(f'https://www.zhipin.com/web/geek/job?query={jobname}&city=100010000&page={i}')
                time.sleep(7)
            if '403' in driver.current_url:
                print("检测到IP被封禁，进行手动登录操作")
                time.sleep(10)
                # 等待手动验证，可以通过检测URL变化或其他方式
                driver_url = driver.current_url
                while 'user' or '403' in driver_url:
                    time.sleep(2)  # 简单地等待1秒再次检查
                    driver_url = driver.current_url
                    print(driver_url)
                print("验证完成，继续执行程序。")
                driver.get(f'https://www.zhipin.com/web/geek/job?query={jobname}&city=100010000&page={i}')
                time.sleep(7)

            content = driver.page_source
            html = etree.HTML(content)
            for output in self.parse_html(html, jobname, filename, df):
                yield output  # 产生输出
            # self.parse_html(html, jobname, filename, df)
            time.sleep(3)  # 等待页面加载
            i += 1
            if i > 5:
                flag = False

        driver.quit()

    def parse_html(self, html, type_name, filename, df):
        li_list = html.xpath('//div[@class="search-job-result"]//ul[@class="job-list-box"]/li')  # 获取职位列表
        for li in li_list:
            job_name = li.xpath('.//span[@class="job-name"]/text()')[0]  # 工作名称
            experiences = li.xpath(
                '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li[1]/div[1]/a/div[2]/ul//text()')  # 年限要求
            if not experiences:
                experiences = li.xpath(
                    '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul/li[1]/div[1]/a/div[2]/ul//text()')  # 年限要求
            # print(experiences)
            experience = experiences[0] if len(experiences) < 3 else experiences[1]
            education = experiences[-1]
            salary = li.xpath('.//div[@class="job-info clearfix"]/span/text()')[0]  # 薪资待遇
            # other = ''
            # detail_url = ''
            company_name = li.xpath('.//div[@class="company-info"]//h3/a/text()')[0]  # 公司名称
            companyinfo = li.xpath('.//div[@class="company-info"]//ul/li//text()')
            if len(companyinfo):
                companyinfo = ''.join(companyinfo)
            # companytype = companyinfo[1] if len(companyinfo)>2 else companyinfo[0] # 公司类型
            location = li.xpath('.//span[@class="job-area"]/text()')[0]  # 工作地点
            words = li.xpath('.//div[@class="job-card-footer clearfix"]/ul[@class="tag-list"]//text()')
            words = ' '.join(words)
            publis_name = li.xpath('.//div[@class="job-info clearfix"]/div[@class="info-public"]//text()')[0]
            publis_name = ''.join(publis_name)
            welfare = li.xpath('.//div[@class="job-card-footer clearfix"]/div[@class="info-desc"]//text()')
            if len(welfare):
                welfare = welfare[0]
            else:
                welfare = ' '
            s = {'type': type_name, 'job_title': job_name, 'job_area': location, 'salary': salary,
                 'condition': experience + education,
                 'company_title': company_name, 'company_info': companyinfo, 'skill': words, 'publis_name': publis_name,
                 'welfare': welfare}
            s_df = pd.DataFrame([s])  # 将字典转换为 DataFrame
            df = pd.concat([df, s_df], ignore_index=True)
            # 产生输出
            yield f"已爬取招聘名称: {job_name}"
        # print(df['job_title'])
        if not os.path.exists(filename):
            # 如果文件不存在，写入列名（header=True）
            df.to_csv(filename, mode='a', index=False, header=True)
        else:
            # 文件已存在，追加数据时不写入列名（header=False）
            df.to_csv(filename, mode='a', index=False, header=False)

def scrape_job_listings(keywords, df):
    boss_instance = Boss()
    for keyword in keywords:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_directory)
        if not os.path.exists('Job_csv'):
            os.makedirs('Job_csv')
        filename = f"Job_csv/{keyword}_job_items.csv"

        # 如果文件存在，则跳过此次循环
        if os.path.exists(filename):
            print(f"文件 {filename} 已存在，跳过此关键词.")
            continue
        # 使用生成器逐步产生输出
        for output in boss_instance.main(keyword, filename, df):
            yield output


def run_crawl():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_directory)
    with open("File/职业.txt", "r", encoding='utf-8') as f:
        data = f.read()
    job_list = data.split('\n')
    df = newcsv()
    # 使用生成器逐步产生输出
    for output in scrape_job_listings(job_list, df):
        yield output

# run_crawl()
# https://www.zhipin.com/web/user/safe/verify-slider