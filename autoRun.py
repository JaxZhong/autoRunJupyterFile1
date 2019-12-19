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

def insert_sql(id, data, content, report_path, alert_info):
    try:
        cur.execute("INSERT INTO `lrqp`.`jupyter_report_log`(`id`, `create_date`, `update_date`, `content`, `report_path`, `alert_info`) VALUES (%s,%s,%s,%s,%s,%s)" , (id, data, data, content, report_path, alert_info))
        conn.commit()
    except:
        conn.rollback()

def sendDingdingQunMsg(report_path, task_name, result):
    url = "https://home.lowrisk.com.cn/ddhelper/rbtMsg"
    headers = {
        'content-type': "application/json"
    }
    payload = {
        "msgtype": "link",
        "link": {
            "messageUrl": "https://home.lowrisk.com.cn/Report/HG" + report_path+"/" + task_name+".html",
            "title": "【任务提醒】 " + task_name + result,
            "text": "系统定时执行"
        },
        "access_token":"8d81b6f2e4bbf5f76215b051724f503003da397bac0c0305e3ca320f2a76568e"
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
        "access_token":"8d81b6f2e4bbf5f76215b051724f503003da397bac0c0305e3ca320f2a76568e"
    }
    response = requests.request("POST", url, data=json.dumps(summary), headers=headers)
    print(response.text)

if __name__ == '__main__':

    conn = pymysql.connect(host = "101.37.33.198",user = "lrqp_db",passwd = "!Lrqp_db20190329",db = "lrqp",charset="utf8")
    cur = conn.cursor()
    sql_query = 'SELECT * FROM jupyter_report_schedule where del_flag = 0 order by create_date desc'
    df = pd.read_sql(sql_query, con=conn)

    for dispatch_cycle,path_all,dispatch_cycle_time_point,path in zip(df['dispatch_cycle'], df['path_all'], df['dispatch_cycle_time_point'], df['path']):
        if('@' in path_all):
            pathAll = path_all.split('@')
            all_path = pathAll[0].split("/")
            name = all_path[len(all_path)-1]
            file_path = path_all + "/" + name + ".ipynb"
            html_path = path_all + "/" + name + ".html"
            report_path = path
            task_name = name

            def run(file_path, report_path, task_name):
                if (os.path.exists(file_path)):
                    today = str(datetime.date.today())
                    uid = str(uuid.uuid4())
                    id = ''.join(uid.split('-'))
                    data = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))

                    newJupyterFile = 'D:/projectFile/lrhg/userfiles/jupyter/temp/' + today + '/' + name + '-' + today + '.ipynb'
                    newHtmlFile = 'D:/projectFile/lrhg/userfiles/jupyter/temp/' + today + '/' + name + '-' + today + '.html'

                    with open(file_path,encoding='utf8') as f:
                        nb = nbformat.read(f, as_version=4)
                    ep = ExecutePreprocessor(timeout=1000, kernel_name='python3')
                    try:
                        # 执行报告
                        out = ep.preprocess(nb, {'metadata': {path_all + '/': 'notebooks/'}})
                    except CellExecutionError as e:
                        # 执行jupyter失败
                        out = None
                        content = "执行jupyter 日志如下：<br/>" + traceback.format_exc().replace("\n","<br/>")
                        alert_info = "执行 "+ task_name +" 失败，运行jupyter报错。请联系IT相关人员"
                        insert_sql(id, data, content, report_path, alert_info)
                        sendDingdingQunMsg(report_path, task_name, " 报告运行报错")
                    else:
                        # 执行成功输出jupyter新报告
                        with open(newJupyterFile, mode='w', encoding='utf-8') as f:
                            nbformat.write(nb, f)

                        # 判断是否已存在html临时文件，存在则删除
                        if (os.path.exists(newHtmlFile)):
                            os.remove(newHtmlFile)

                        # 将输出新报告转成html文件
                        os.system("jupyter nbconvert --to html --TemplateExporter.exclude_input=True  --TemplateExporter.exclude_output_prompt=True "+ newJupyterFile +" --output " + newHtmlFile)

                        # 如果产生新html文件则转html成功
                        if (os.path.exists(newHtmlFile)):
                            content = ""
                            alert_info = "执行 "+ task_name +"报告 成功"
                            insert_sql(id, data, content, report_path, alert_info)
                            sendDingdingQunMsg(report_path, task_name, " 成功")
                            sendSummaryReport(html_path,task_name)
                        else:
                            content = ""
                            alert_info = "执行 "+task_name+" 失败，将jupyter转html报错。请联系IT相关人员";
                            insert_sql(id, data, content, report_path, alert_info)
                            sendDingdingQunMsg(report_path, task_name, "报告将jupyter转html报错。请联系IT相关人员")
                else:
                    print("jupyter源文件" + file_path + "不存在，请联系IT相关人员")
                    sendDingdingQunMsg(report_path, report_path, "jupyter源文件不存在，请联系IT相关人员")

            if(dispatch_cycle == '1'):
                run(file_path, report_path, task_name)
            elif(dispatch_cycle == '2'):
                if(int(dispatch_cycle_time_point) == datetime.datetime.now().isoweekday()):
                    run(file_path, report_path, task_name)
            elif(dispatch_cycle == '3'):
                if(int(dispatch_cycle_time_point) == datetime.datetime.now().day):
                    run(file_path, report_path, task_name)
    conn.close()

