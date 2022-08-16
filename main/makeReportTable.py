from collections import defaultdict


def make(dic, datelist):
    #data가 들어오면 model(감마, 베타, 세타 등)별로 list를 만든다 가정. dic() , {"감마" : [k1, k2, k3, k4 ....]}
    #이때 key값은 modellist
    colors = ["#eeb7b4", "#f2cfa5", "#fcffb0", "#aee4ff", "#b5c7ed", "#c4f4fe", "#bee9b4"
        , "#fdfa87", "#fcc6f7", "#caa6fe", "#ffafd8", "#afffba", "#e2ffaf", "#fcffb0", "#f2cfa5", "#ffe4af"]
    result = "<table>"
    result += header(datelist)
    #시작날짜이후의 데이터만 받아옴
    colorcnt = 0
    for k, v in dic.items():
        result += mtable(datelist, k, v, colors[colorcnt%16])
        colorcnt += 1
    return result + "</table>"


def header(datelist):
    s = "<thead><tr class='testtr'><td colspan='2'>엔진사양</td><td>구분</td><td>이월재고</td>"
    #datalist가 20220728 과같이 들어온다고 가정
    for i in datelist:
        s += "<td>"+i[4:6]+"/"+i[6:]+"</td>"
    return s + "<td>합계</td></tr></thead>"


def mtableheader(datelist, model, l, color):
    s = "<tr><td colspan='2' rowspan='3' style='background-color:"+color+"'>"+model+"</td><td class='reportTableTd'>입고계</td><td></td>"
    for d in datelist:
        s += "<td>"+inputcell(d, l)+"</td>"
    s += "<td>"+inputsum(datelist[0], datelist[-1], l)+"</td></tr><tr><td class='reportTableTd'>불출계</td><td></td>"
    for d in datelist:
        s += "<td>"+outputcell(d, l)+"</td>"
    s += "<td>"+outputsum(datelist[0], datelist[-1], l)+"</td></tr><tr><td class='reportTableTd'>재고계</td>"
    s += "<td style='background-color:#FDFD96'>"+basiccell(datelist[0], l)+"</td>"
    for d in datelist:
        s += "<td>"+stockcell(d, l)+"</td>"
    return s + "<td>"+stockcell(datelist[-1], l)+"</td></tr>"


def mtablebody(datelist, dic):
    row_l = len(dic)
    s = "<tr><td rowspan='"+str(row_l*3)+"'>&nbsp;&nbsp;&nbsp;&nbsp;</td>"
    for k, v in dic.items():
        s += "<td rowspan='3'>"+str(k)+"</td><td>입고</td><td></td>"
        for d in datelist:
            s += "<td>"+inputcell(d, v)+"</td>"
        s += "<td>"+inputsum(datelist[0], datelist[-1], v)+"</td></tr><tr><td>출고</td><td></td>"
        for d in datelist:
            s += "<td>"+outputcell(d, v)+"</td>"
        s += "<td>"+outputsum(datelist[0], datelist[-1], v)+"</td></tr><tr><td>재고</td>"
        s += "<td style='background-color:#FFFFDD'>" + basiccell(datelist[0], v) + "</td>"
        for d in datelist:
            s += "<td>"+stockcell(d, v)+"</td>"
        s += "<td>"+stockcell(datelist[-1], v)+"</td></tr>"
    return s


def mtable(datelist, k, v, color):
    model = str(k)
    dic = defaultdict(list)
    s = ""
    for i in v:
        dic[i[0]].append([i[1], i[2]])
    s += mtableheader(datelist, model, sum(dic.values(), []), color)
    s += mtablebody(datelist, dic)
    return s


def inputcell(day, l):
    cnt = 0
    for i in l:
        if str(i[0]) == day:
            cnt += 1
    if cnt == 0:
        return "-"
    return str(cnt)


def outputcell(day, l):
    cnt = 0
    for i in l:
        if str(i[1]) == day:
            cnt += 1
    if cnt == 0:
        return "-"
    return str(cnt)


def stockcell(day, l):
    cnt = 0
    for i in l:
        if (i[1] is None) and (int(i[0]) <= int(day)):
            cnt += 1
        elif (int(i[0]) <= int(day)) and (int(i[1]) > int(day)):
            cnt += 1
    if cnt == 0:
        return "-"
    return str(cnt)


def inputsum(sday, eday, l):
    cnt = 0
    for i in l:
        if (int(i[0]) >= int(sday)) and (int(i[0]) <= int(eday)):
            cnt += 1
    if cnt == 0:
        return "-"
    return str(cnt)


def outputsum(sday, eday, l):
    cnt = 0
    for i in l:
        if (i[1] == "") or (i[1] is None):
            continue
        if (int(i[1]) >= int(sday)) and (int(i[1]) <= int(eday)):
            cnt += 1
    if cnt == 0:
        return "-"
    return str(cnt)


def basiccell(day, l):
    # 이월 재고 계산
    a = outputcell(day, l)
    b = inputcell(day, l)
    c = stockcell(day, l)
    if a == "-":
        a = 0
    if b == "-":
        b = 0
    if c == "-":
        c = 0
    return str(int(a) + int(c) - int(b))
