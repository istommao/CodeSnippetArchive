"""日期相关代码片段."""
import datetime


def get_start_of_today():
    """获取今天的开始时间."""
    return datetime.datetime.combine(datetime.date.today(), datetime.time.min)


def get_end_of_today():
    """获取今天的结束时间."""
    return datetime.datetime.combine(datetime.date.today(), datetime.time.max)
