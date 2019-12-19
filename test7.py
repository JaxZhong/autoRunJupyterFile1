
import json
import requests

def sendDingdingQunMsg(report_path, task_name):
    url = "https://home.lowrisk.com.cn/ddhelper/rbtMsg"
    headers = {
        'content-type': "application/json"
    }
    payload = {
        "msgtype": "link",
        "link": {
            "messageUrl": "https://home.lowrisk.com.cn/Report/HG"+"/"+report_path+"/"+task_name+".html",
            "title": "【任务提醒】 " + task_name + " 成功",
            "text": "执行人：" + this.getCreateBy().getName(),
            "access_token":"8d81b6f2e4bbf5f76215b051724f503003da397bac0c0305e3ca320f2a76568e"
        }
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)

if __name__ == '__main__':
    sendDingdingQunMsg()
