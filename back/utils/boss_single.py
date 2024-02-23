import asyncio  # 异步编程库
import os
import random  # 随机数生成库
from pyppeteer import launch  # 网页自动化测试库
from lxml import etree  # XML和HTML解析库
import pandas as pd


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

    # 新建CSV文件

    async def main(self, jobname, filename, df):
        browser = await launch(
            headless=False,  # 是否无头模式（可见/不可见浏览器）
            userDataDir="./config",  # 用户数据目录（用于保持浏览器会话）
            args=['--disable-infobars', '--window-size=1366,768', '--no-sandbox']  # 启动参数
        )

        page = await browser.newPage()  # 创建新页面
        width, height = self.screen_size()  # 获取屏幕大小
        await page.setViewport({'width': width, 'height': height})  # 设置页面视口大小

        await page.goto(
            'https://www.zhipin.com/?city=' + '100010000' + '&ka=city-sites-100010000')  # 打开目标网页
        await page.evaluateOnNewDocument(
            '''() =>{ Object.defineProperties(navigator, { webdriver: { get: () => false } }) }'''
        )  # 修改浏览器环境，防止被检测为自动化测试工具
        await asyncio.sleep(5)  # 等待页面加载

        i = 1
        flag = True
        while flag:
            print(i, '页', filename)
            await page.goto(
                'https://www.zhipin.com/web/geek/job?query=' + jobname + '&city=' + '100010000' + '&page=' + str(
                    i))  # 打开目标网页
            await page.evaluateOnNewDocument(
                '''() =>{ Object.defineProperties(navigator, { webdriver: { get: () => false } }) }'''
            )  # 修改浏览器环境，防止被检测为自动化测试工具
            await asyncio.sleep(3)  # 等待页面加载
            content = await page.content()  # 获取页面内容
            html = etree.HTML(content)  # 解析页面内容
            self.parse_html(html, jobname, filename, df)  # 解析内容
            await asyncio.sleep(3)  # 等待页面加载
            i += 1
            # boss直聘限制翻页为10页，分省分批次抓取
            if i > 5:
                flag = False
        if browser:
            await browser.close()  # Ensure the browser is closed.

    def input_time_random(self):
        return random.randint(100, 151)  # 生成随机的输入延迟时间

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

        print(df)
        if not os.path.exists(filename):
            # 如果文件不存在，写入列名（header=True）
            df.to_csv(filename, mode='a', index=False, header=True)
        else:
            # 文件已存在，追加数据时不写入列名（header=False）
            df.to_csv(filename, mode='a', index=False, header=False)

        # with open(filename, encoding = 'utf-8', mode = 'a', newline = '') as f:
        #     csv_writer = csv.writer(f)
        #     csv_writer.writerow(
        #         [job_name, experience, education, salary, company_name, companytype, numbers, location,
        #          words])

    def run(self, jobname, filename, df):
        asyncio.get_event_loop().run_until_complete(self.main(jobname, filename, df))  # 运行异步任务


async def scrape_job_listings(keywords, df):
    boss_instance = Boss()
    for keyword in keywords:
        if not os.path.exists('Job_csv'):
            os.makedirs('Job_csv')
        filename = f"Job_csv/" + keyword + "_job_items.csv"
        if os.path.exists(filename):  # 存在此文件，爬过了，跳过
            print(filename + "存在此文件,爬过了，跳过")
            continue
        await boss_instance.main(keyword, filename, df)


if __name__ == '__main__':
    with open("File/职业.txt", "r", encoding='utf-8') as f:  # 打开文件
        data = f.read()  # 读取文件
    job_list = data.split('\n')
    df = newcsv()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_job_listings(job_list, df))
