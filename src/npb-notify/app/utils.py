import datetime


def conv_ave(val: str) -> float:
    return float(val) if val == '1' else float('0' + val)


def conv_date(val: str) -> datetime.date:
    return datetime.datetime.strptime(val, '%m月%d日').date()
