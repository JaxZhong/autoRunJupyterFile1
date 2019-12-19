import datetime


if __name__ == '__main__':
    def last_day_of_month(any_day):
        """
        获取获得一个月中的最后一天
        :param any_day: 任意日期
        :return: string
        """
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)

    # 注意: 年月日，这些变量必须是数字，否则报错！
    year = 2019 # 年
    month = 12  # 月
    day = 31 # 日

    if(2 >= 2):
        print("ssdfdsf")

    res = last_day_of_month(datetime.date.today())
    print(res)