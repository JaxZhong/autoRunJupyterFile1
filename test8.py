#coding=utf-8
from bs4 import BeautifulSoup


if __name__ == '__main__':
    soup = BeautifulSoup(open('D:/jupyter/宏观团队/HG/1.高频跟踪/1.周度宏观跟踪@/1.周度宏观跟踪.html',encoding='utf8'), 'html.parser')# 获取被抓取页面的html代码（注意这里是用 request框架获取的页面源码），并使用html.parser来实例化BeautifulSoup，属于固定套路
    a = []
    for course in soup.find_all('div', class_='cell border-box-sizing code_cell rendered'):# 遍历页面上所有的h4标签
        if(course.div != None):
            a = course.div;

    html = "<html><body>"+str(a)+"</body></html>"
    if("触发汇总" in html):
        print("fdsfsdaf")