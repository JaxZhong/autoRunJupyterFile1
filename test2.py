import threading
import datetime

if __name__ == '__main__':
    def do_job():
        print('Just do it!')
        global timer
        timer = threading.Timer(86400, do_job) # 86400秒就是一天
        timer.start()

    # 计算当前时间到明日某时间的秒数差
    def get_interval_secs():
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')
        tomorrow_time = tomorrow + "-09:00:00"
        tomorrow_time_date = datetime.datetime.strptime(tomorrow_time, '%Y%m%d-%H:%M:%S')
        now = datetime.datetime.now()
        interval = tomorrow_time_date - now
        secs = interval.total_seconds()
        return secs

    # 测试计算到今日某时的时间差
    def get_interval_secs_test():
        today = (datetime.date.today()).strftime('%Y%m%d')
        today_time = today + "-16:16:00"
        today_time_date = datetime.datetime.strptime(today_time, '%Y%m%d-%H:%M:%S')
        now = datetime.datetime.now()
        print(now)
        interval = today_time_date - now
        secs = interval.total_seconds()
        return secs

    timer = threading.Timer(2, do_job)
    timer.start()