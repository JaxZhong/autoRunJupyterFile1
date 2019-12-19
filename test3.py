import datetime
import time

if __name__ == '__main__':




    print(time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())))
    dayOfWeek = datetime.datetime.now().isoweekday() ###返回数字1-7代表周一到周日
    day_Week = datetime.datetime.now().weekday() ###返回从0开始的数字，比如今天是星期5，那么返回的就是4
    day = datetime.datetime.now()
    today = str(datetime.date.today())
    print(today)
    print(type(dayOfWeek) )
    print(day_Week )
    print(day )