from collections import defaultdict


def make(dic, datelist):
    #data가 들어오면 model(감마, 베타, 세타 등)별로 list를 만든다 가정. dic() , {"감마" : [k1, k2, k3, k4 ....]}
    #이때 key값은 modellist
    result = "<table>"
    result += header(datelist)
    #시작날짜이후의 데이터만 받아옴
    for k, v in dic.items():
        result += mtable(datelist, k, v)
    return result + "</table>"


def header(datelist):
    s = "<thead><tr><td>엔진사양</td><td>구분</td>"
    #datalist가 20220728 과같이 들어온다고 가정
    for i in datelist:
        s += "<td>"+i[4:6]+"/"+i[6:]+"</td>"
    return s + "</tr></thead>"


def mtableheader(datelist, model):
    s = "<tr><td colspan='2' rowspan='3'>"+model+"</td><td>입고계</td>"
    for d in datelist:
        s += "<td></td>"
    s += "</tr><tr><td>불출계</td>"
    for d in datelist:
        s += "<td></td>"
    s += "</tr><tr><td>재고계</td>"
    for d in datelist:
        s += "<td></td>"
    return s + "</tr>"


def mtablebody(datelist, dic):
    row_l = len(dic)
    s = "<tr><td rowspan='"+str(row_l*3)+"'></td>"
    for k, v in dic.items():
        s += "<td rowspan='3'>"+str(k)+"</td><td>입고</td>"
        for d in datelist:
            # + cells, 각 날짜에 맞는 수량들
            s += "<td></td>"
        s += "</tr><tr><td>출고</td>"
        for d in datelist:
            # + cells, 각 날짜에 맞는 수량들
            s += "<td></td>"
        s += "</tr><tr><td>재고</td>"
        for d in datelist:
            # + cells, 각 날짜에 맞는 수량들
            s += "<td></td>"
        s += "</tr>"
    return s


def mtable(datelist, k, v):
    model = str(k)
    dic = defaultdict(list)
    s = ""
    for i in v:
        dic[i[0]].append([i[1], i[2]])
    s += mtableheader(datelist, model)
    s += mtablebody(datelist, dic)
    return s


def inputcell(day, l):
    return 1


def outputcell(day, l):
    return 1