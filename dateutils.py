import datetime

def parse_date(date):
    y = int(date[0:4])
    m = int(date[4:6])
    d = int(date[6:8])
    return datetime.date(y, m, d)

def split_time(time):
    time_parts = time.split(':')
    return (int(time_parts[0]), int(time_parts[1]), int(time_parts[2]))

def parse_time(time):
    time_parts = split_time(time)
    return datetime.time(time_parts[0], time_parts[1], time_parts[2])

def build_datetime(year, month, day, hour, minute, second):
    add_day = datetime.timedelta(0)
    if hour > 23:
        hour = hour - 24
        add_day = datetime.timedelta(1)
    return datetime.datetime(year, month, day, hour, minute, second) + add_day
        