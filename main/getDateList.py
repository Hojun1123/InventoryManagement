from datetime import date, timedelta


def datelist(start, end):
    dl = []
    s = date(int(start[0:4]), int(start[4:6]), int(start[6:8]))
    e = date(int(end[0:4]), int(end[4:6]), int(end[6:8]))
    delta = e - s
    for i in range(delta.days + 1):
        dl.append((s + timedelta(days=i)).strftime("%Y%m%d"))
    return dl
