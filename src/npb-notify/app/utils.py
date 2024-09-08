import datetime


def conv_ave(val: str) -> float:
    if val == '1':
        return 1.0
    elif val[0] == '.':
        return float('0' + val)
    else:
        return -1.0


def conv_date(val: str) -> datetime.date:
    return datetime.datetime.strptime(val, '%m月%d日').date()
