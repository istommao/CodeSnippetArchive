"""日期相关代码片段."""
import datetime


# 日期格式化


now = datetime.datetime.now()
now.strftime('%Y-%m-%d %H:%M:%S')


# 字符串转日期
datestr = '2016-03-15 19:38:17'
datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
datetime.datetime(2016, 3, 15, 19, 38, 17)

# 获取一天的开始与结尾


def get_start_of_today():
    """获取今天的开始时间."""
    return datetime.datetime.combine(datetime.date.today(), datetime.time.min)


def get_end_of_today():
    """获取今天的结束时间."""
    return datetime.datetime.combine(datetime.date.today(), datetime.time.max)


# 获取上个月


def get_last_month_range():
    end = datetime.date.today().replace(day=1) - datetime.timedelta(1)
    start = end.replace(day=1)
    return datetime.datetime.combine(start, datetime.time.min), datetime.datetime.combine(end, datetime.time.max)


# 获取第n个月
def get_month_range(n):
    today = datetime.date.today()
    year_diff = (today.month + n) // 12
    end = today.replace(
        month=(today.month + n) % 12 + 1,
        year=today.year + year_diff,
        day=1
    ) - datetime.timedelta(days=1)

    start = end.replace(day=1)
    return datetime.datetime.combine(start, datetime.time.min), datetime.datetime.combine(end, datetime.time.max)
