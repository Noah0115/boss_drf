# 环境配置及功能模块说明

## 项目环境

Python3.11.6

Windows11

Pycharm专业版

Mysql8

后端框架:django4

## 环境配置


**请确保进行此步骤前，配置好python与mysql8的环境**
打开Pycharm，打开项目，设置项目解释器为Python3.11.6
在pycharm中打开终端输入来安装依赖

```python
pip install -r requirements.txt
```

接着在pycharm中进行如下设置：

<img src="https://immich.lyh27.top/api/assets/24b1343c-7148-4d1f-8694-dc65b186dbbd/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130174735538" />

<img src="https://immich.lyh27.top/api/assets/a5d8f99b-da5e-4215-a158-0532b8fa7e26/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130180447231" />

到boss_drf文件夹下，打开settings.py，进行数据库连接修改

<img src="https://immich.lyh27.top/api/assets/60deaff6-1212-4c81-a8ed-cb065094ad83/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130183027351" />

然后，打开终端，输入

```python
python manage.py makemigrations
python manage.py migrate
```

<img src="https://immich.lyh27.top/api/assets/4b6df0c2-c209-4e59-b2be-000bad231cc8/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182855863" />

确定后，点击运行即可

<img src="https://immich.lyh27.top/api/assets/a3840c1f-c95f-44d4-8b69-d916d04e879c/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130180638459" />

浏览器访问 http://127.0.0.1:7000/

<img src="https://immich.lyh27.top/api/assets/171a0869-dfaa-4b9c-b91e-02ba8efa3ba8/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130180732556" />

## 模块介绍

### 在线爬取

进入”在线爬取“模块，点击开始爬虫，自动与后端建立websocket连接，前端页面显示爬虫的实时爬取信息状态

点击停止爬虫，关闭websocket，**想要停止爬虫的时候，一定要点击停止爬虫，不要切换页面，如果切换页面爬虫程序是依然在后台运行的，会导致影响其他模块。**

另外，back/utils/boss_single.py这个文件是可以脱离django项目单独运行的boss直聘爬虫，如果以前端的方式爬虫较慢的话，可以先执行此py文件单独将数据爬取下来，然后启动项目，跳过在线爬虫模块，直接进行数据预处理模块，是一样的，只不过形式不同。

**注意：由于其他模块的数据都依赖于此功能模块，务必保证爬虫完整运行，最好不要中途停止，否则影响数据预处理与数据分析、职业预测，同时不要关闭自动弹出的chrome浏览器，否则爬虫运行失败。(点击停止爬虫，稍等一会才会自动停止，同时chrome浏览器会自动关闭)**

<img src="https://immich.lyh27.top/api/assets/073ae34c-0370-4f60-bf55-819df62d55e9/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130181344149" />

### 数据预处理

保证“在线爬取”模块完整运行后，进入“数据预处理”模块，首先点击“数据预处理”，对爬下来的招聘信息进行数据清洗与预处理

<img src="https://immich.lyh27.top/api/assets/611e55a3-d1a4-49e5-843f-eac8cf20a356/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182029762" />

<img src="https://immich.lyh27.top/api/assets/a11965a8-f7ee-4aca-be61-f838c4eaf062/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182048580" />

处理完毕后，接着点击“数据库导入”，将数据导入到back_jobinfo数据库表中

<img src="https://immich.lyh27.top/api/assets/499b4fe1-6f1f-4e2d-bf08-501b8c46aaf3/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182202052" />

<img src="https://immich.lyh27.top/api/assets/9cf6ba69-0a22-41dd-9a45-f12ec786d421/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182215780" />

<img src="https://immich.lyh27.top/api/assets/10717490-b3e2-48f9-9cb2-8f6b602b138a/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182235726" />

### 数据查询

<img src="https://immich.lyh27.top/api/assets/bf6bb35d-22f5-4f62-8f9a-a474657c260a/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182323054" />

### 岗位/地区平均工资

<img src="https://immich.lyh27.top/api/assets/b3fb388d-21a0-42a6-96bf-8b5b556b59ed/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182350657" />

![image-20240130182401509](http://sapic.lyh27.top/static/upload/admin/image-20240130182401509.png)

### 地区热门职位

<img src="https://immich.lyh27.top/api/assets/38a455ca-b4bc-4108-a83d-2ec020443aff/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182420868" />

### 地区招聘数量

<img src="https://immich.lyh27.top/api/assets/1d9dbf1d-6e2b-494a-989f-44924e5afd8a/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182439216" />

### 岗位学历/经验要求

<img src="https://immich.lyh27.top/api/assets/85fcc498-0a3a-4fcc-86a9-361d8f495535/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182501863" />

### 职业预测

进入"职业预测"模块，选择你的技术栈，后端返回预测适合职业的概率

<img src="https://immich.lyh27.top/api/assets/08bad591-1710-4aee-bca6-f9e05e6fd726/thumbnail?size=preview&key=25V6Vu9F_RRr2dJRHv9neJzgAYlcc4v8m9nc51VCXZcwhXYMn8GwtfaJuVsBitUCJq8" alt="image-20240130182625536" />

## 感谢
前端可视化部分原作者[@BATFOR](https://github.com/BATFOR)

爬虫部分原作者[@MT-BOX](https://github.com/MT-BOX)

本项目基于两位作者的基础上进行代码更新及修改。
