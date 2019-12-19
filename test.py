import os
import pymysql
import pandas as pd
import datetime
import uuid
import time

if __name__ == '__main__':
    conn = pymysql.connect(host = "101.37.33.198",user = "lrqp_db",passwd = "!Lrqp_db20190329",db = "lrqp",charset="utf8")
    cur = conn.cursor()
    uid = str(uuid.uuid4())
    id = ''.join(uid.split('-'))
    time = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
    content = "asdasdasd"
    path_all = "sfsdfweqafqwe"
    try:
        cur.execute("INSERT INTO `lrqp`.`jupyter_report_log`(`id`, `create_date`, `update_date`, `content`, `report_path`) VALUES (%s,%s,%s,%s,%s)" , (id, time, time, content, path_all))
        conn.commit()
    except:
        conn.rollback()
        print("sadas")
    finally:
        conn.close()