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

![image-20240130174735538](http://sapic.lyh27.top/static/upload/admin/image-20240130174735538.png)

![image-20240130180447231](http://sapic.lyh27.top/static/upload/admin/image-20240130180447231.png)

到boss_drf文件夹下，打开settings.py，进行数据库连接修改

![image-20240130183027351](http://sapic.lyh27.top/static/upload/admin/image-20240130183027351.png)

然后，打开终端，输入

```python
python manage.py makemigrations
python manage.py migrate
```

![image-20240130182855863](http://sapic.lyh27.top/static/upload/admin/image-20240130182855863.png)

确定后，点击运行即可

![image-20240130180638459](http://sapic.lyh27.top/static/upload/admin/image-20240130180638459.png)

浏览器中打开http://127.0.0.1:7000/来访问页面

![image-20240130180732556](http://sapic.lyh27.top/static/upload/admin/image-20240130180732556.png)

## 模块介绍

### 在线爬取

进入”在线爬取“模块，点击开始爬虫，自动与后端建立websocket连接，前端页面显示爬虫的实时爬取信息状态

点击停止爬虫，关闭websocket，**想要停止爬虫的时候，一定要点击停止爬虫，不要切换页面，如果切换页面爬虫程序是依然在后台运行的，会导致影响其他模块。**

另外，back/utils/boss_single.py这个文件是可以脱离django项目单独运行的boss直聘爬虫，如果以前端的方式爬虫较慢的话，可以先执行此py文件单独将数据爬取下来，然后启动项目，跳过在线爬虫模块，直接进行数据预处理模块，是一样的，只不过形式不同。

**注意：由于其他模块的数据都依赖于此功能模块，务必保证爬虫完整运行，最好不要中途停止，否则影响数据预处理与数据分析、职业预测，同时不要关闭自动弹出的chrome浏览器，否则爬虫运行失败。(点击停止爬虫，稍等一会才会自动停止，同时chrome浏览器会自动关闭)**

![image-20240130181344149](http://sapic.lyh27.top/static/upload/admin/image-20240130181344149.png)

### 数据预处理

保证“在线爬取”模块完整运行后，进入“数据预处理”模块，首先点击“数据预处理”，对爬下来的招聘信息进行数据清洗与预处理

![image-20240130182029762](http://sapic.lyh27.top/static/upload/admin/image-20240130182029762.png)

![image-20240130182048580](http://sapic.lyh27.top/static/upload/admin/image-20240130182048580.png)

处理完毕后，接着点击“数据库导入”，将数据导入到back_jobinfo数据库表中

![image-20240130182202052](http://sapic.lyh27.top/static/upload/admin/image-20240130182202052.png)

![image-20240130182215780](http://sapic.lyh27.top/static/upload/admin/image-20240130182215780.png)

![image-20240130182235726](http://sapic.lyh27.top/static/upload/admin/image-20240130182235726.png)

### 数据查询

![image-20240130182323054](http://sapic.lyh27.top/static/upload/admin/image-20240130182323054.png)

### 岗位/地区平均工资

![image-20240130182350657](http://sapic.lyh27.top/static/upload/admin/image-20240130182350657.png)

![image-20240130182401509](http://sapic.lyh27.top/static/upload/admin/image-20240130182401509.png)

### 地区热门职位

![image-20240130182420868](http://sapic.lyh27.top/static/upload/admin/image-20240130182420868.png)

### 地区招聘数量

![image-20240130182439216](http://sapic.lyh27.top/static/upload/admin/image-20240130182439216.png)

### 岗位学历/经验要求

![image-20240130182501863](http://sapic.lyh27.top/static/upload/admin/image-20240130182501863.png)

### 职业预测

进入"职业预测"模块，选择你的技术栈，后端返回预测适合职业的概率

![image-20240130182625536](http://sapic.lyh27.top/static/upload/admin/image-20240130182625536.png)

## 感谢
前端可视化部分原作者[@BATFOR](https://github.com/BATFOR)

爬虫部分原作者[@MT-BOX](https://github.com/MT-BOX)

本项目基于两位作者的基础上进行代码更新及修改。
