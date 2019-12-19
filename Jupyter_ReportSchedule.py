#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/15 0015 22:29
# @Author  : Jax
# @Site    : 
# @File    : Jupyter_ReportSchedule.py

import os
import pymysql
import pandas as pd
import datetime
import uuid
import nbformat
import traceback
import time
import json
import requests
from bs4 import BeautifulSoup
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError


today = str(datetime.date.today())
BASE_PATH = 'D:/projectFile/lrhg/userfiles/jupyter/temp/' + today + '/'
token = "XXXXXXXXXXXX"

if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

conn = pymysql.connect(host = "101.37.33.198",user = "lrqp_db",passwd = "XXXXXXXXXXXX",db = "lrqp",charset="utf8")
cur = conn.cursor()


def last_day_of_month(any_day):
    """
    获取获得一个月中的最后一天
    :param any_day: 任意日期
    :return: string
    """
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

def insert_sql(id, create_date, content, report_path, alert_info):
    try:
        cur.execute("INSERT INTO `lrqp`.`jupyter_report_log`(`id`, `create_date`, `update_date`, `create_by`, `update_by`, `content`, `report_path`, `alert_info`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" , (id, create_date, create_date, '1', '1', content, report_path, alert_info))
        conn.commit()
    except:
        conn.rollback()

def sendDingdingQunMsg(report_path, task_name, status, result):
    url = "XXXXXXXXXXXX"
    headers = {
        'content-type': "application/json"
    }
    payload = {
        "msgtype": "link",
        "link": {
            "messageUrl": "https://home.lowrisk.com.cn/Report/HG" + report_path+"/" + task_name+".html",
            "title": status + task_name + result,
            "text": "系统定时执行"
        },
        "access_token" : token
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)

def sendSummaryReport(html_path,task_name):

    soup = BeautifulSoup(open(html_path,encoding='utf8'), 'html.parser')
    summ = []
    for course in soup.find_all('div', class_='cell border-box-sizing code_cell rendered'):
        if(course.div != None):
            summ = course.div;
    html = "<html><body>"+str(summ)+"</body></html>"
    if("触发汇总" in html):
        # TODO html转图片对象储存链接image_url
        image_url = ""

    url = "https://home.lowrisk.com.cn/ddhelper/rbtMsg"
    headers = {
        'content-type': "application/json"
    }
    summary = {
        "msgtype": "markdown",
        "markdown": {
            "title": task_name,
            "text": "![](" + image_url + ")"
        },
        "access_token" : token
    }
    response = requests.request("POST", url, data=json.dumps(summary), headers=headers)
    print(response.text)


def run(file_path, report_path, task_name):
    success = "【任务提醒】 "
    error = "【Error提醒】 "
    if (os.path.exists(file_path)):
        uid = str(uuid.uuid4())
        id = ''.join(uid.split('-'))
        create_date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))

        newJupyterFile = BASE_PATH + name + '-' + today + '.ipynb'
        newHtmlFile = BASE_PATH + name + '-' + today + '.html'

        with open(file_path, encoding='utf8') as f:
            nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=1000, kernel_name='python3')
        try:
            # 执行报告
            print('begin running jupyter .....')
            out = ep.preprocess(nb, {'metadata': {path_all + '/': 'notebooks/'}})
        except CellExecutionError as e:
            # 执行jupyter失败
            out = None
            content = "执行jupyter 日志如下：<br/>" + traceback.format_exc().replace("\n", "<br/>")
            alert_info = "执行 " + task_name + " 失败，运行jupyter报错。请联系IT相关人员"
            insert_sql(id, create_date, content, report_path, alert_info)
            sendDingdingQunMsg(report_path, task_name, error, " 报告运行报错")
        else:
            # 执行成功输出jupyter新报告
            with open(newJupyterFile, mode='w', encoding='utf-8') as f:
                nbformat.write(nb, f)
                # 【Error提醒】
            # 判断是否已存在html临时文件，存在则删除
            if (os.path.exists(newHtmlFile)):
                os.remove(newHtmlFile)

            # 将输出新报告转成html文件
            os.system(
                "jupyter nbconvert --to html --TemplateExporter.exclude_input=True  --TemplateExporter.exclude_output_prompt=True " + newJupyterFile + " --output " + newHtmlFile)

            # 如果产生新html文件则转html成功
            if (os.path.exists(newHtmlFile)):
                content = ""
                alert_info = "执行 " + task_name + "报告 成功"
                insert_sql(id, create_date, content, report_path, alert_info)

                # TODO  复制文件操作

                sendDingdingQunMsg(report_path, task_name, success, " 成功")
                sendSummaryReport(html_path, task_name)
            else:
                content = ""
                alert_info = "执行 " + task_name + " 失败，将jupyter转html报错。请联系IT相关人员";
                insert_sql(id, create_date, content, report_path, alert_info)
                sendDingdingQunMsg(report_path, task_name, error, "报告将jupyter转html报错。请联系IT相关人员")
    else:
        print("jupyter源文件" + file_path + "不存在，请联系IT相关人员")
        sendDingdingQunMsg(report_path, report_path, error, "jupyter源文件不存在，请联系IT相关人员")

if __name__ == '__main__':


    sql_query = 'SELECT * FROM jupyter_report_schedule where del_flag = 0 order by create_date desc'
    df = pd.read_sql(sql_query, con=conn)

    for dispatch_cycle,path_all,dispatch_cycle_time_point,path in zip(df['dispatch_cycle'], df['path_all'], df['dispatch_cycle_time_point'], df['path']):
        print(path_all)
        pathAll = path_all.split('@')
        all_path = pathAll[0].split("/")
        name = all_path[len(all_path)-1]
        file_path = path_all + "/" + name + ".ipynb"
        html_path = path_all + "/" + name + ".html"
        report_path = path
        task_name = name
        print(task_name)
        if(dispatch_cycle == '1'):
            print('day:'+task_name)
            run(file_path, report_path, task_name)
        elif(dispatch_cycle == '2'):
            if(int(dispatch_cycle_time_point) == datetime.datetime.now().isoweekday()):
                print('week:'+task_name)
                run(file_path, report_path, task_name)
        elif(dispatch_cycle == '3'):
            if(today == last_day_of_month(today)):
                if(int(dispatch_cycle_time_point) >= datetime.datetime.now().day):
                    print('month:'+task_name)
                    run(file_path, report_path, task_name)
            elif(int(dispatch_cycle_time_point) == datetime.datetime.now().day):
                print('month:'+task_name)
                run(file_path, report_path, task_name)
    conn.close()
