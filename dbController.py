# db control
import threading
import datetime
import openpyxl as op
from collections import defaultdict
import pandas as pd
import math
import numpy as np


def open_sheet(file, sheet):
    rb = op.load_workbook("./DB/" + file + ".xlsx")
    return rb[sheet]


def open_file(file):
    return op.load_workbook("./DB/" + file + ".xlsx")


def get_path(file):
    return "./DB/" + file + ".xlsx"


#마지막 동기화 시간 반환
def last_sync_time():
    try:
        rs = open_sheet("barcode", "rawBarcode")
    except:
        print("can't open barcode.xlsx")
        return -1
    return [i.value for i in list(rs.rows)[-1][1:3]]


def append_raw_barcodes(data):
    try:
        wb1 = open_file("barcode")
    except:
        print("can't open barcode.xlsx")
        return -1
    w1s1 = wb1["rawBarcode"]
    c = 0
    sl = len(list(w1s1.rows))
    tm = datetime.datetime.now()
    date = tm.strftime("%Y%m%d")
    time = (tm.strftime("%X"))[0:2] + (tm.strftime("%X"))[3:5] + (tm.strftime("%X"))[6:8]
    for i in data:
        c += 1
        gi = sl + c
        # gk, location
        for j in i:
            # 엔진시리얼번호, 바코드, 날짜, 시간, 그룹ID
            w1s1.append([j, date, time, str(gi)])
    wb1.save(get_path("barcode"))
    wb1.close()


def get_data_to_add(day, time):
    try:
        wb = open_sheet("barcode", "rawBarcode")
    except:
        print("can't open barcode.xlsx")
        return -1
    data = []
    dlist = list(wb.rows)
    for i in range(1, len(dlist)):
        if int(dlist[i][1].value) > int(day):
            #barcode, date, gid
            data.append([dlist[i][0], dlist[i][1], dlist[i][3]])
        elif (int(dlist[i][1].value) == int(day)) and (int(dlist[i][2].value)+100000 > int(time)+100000):
            data.append([dlist[i][0], dlist[i][1], dlist[i][3]])
        else:
            continue
    if len(data) < 1:
        print("no exist data to add")
        return 0
    return data


# engineController
def get_sync_time():
    try:
        ws = open_sheet("engine", "syncTime")
        return [i.value for i in list(ws.rows)[0][0:2]]
    except:
        print("can't read syncTime ")
        return -1


def get_type(mip):
    try:
        rs = open_sheet("engine", "types")
    except:
        print("can't read types")
        return -1
    for row in rs.rows:
        # empty rows 탐색 제외
        if row[0].value is None:
            break
        if row[0].value == mip:
            return row[1].value
    print("Invalid MIP")
    return -1


#barcode.xlsx 를 engine.xlsx에 동기화
def synchronization():
    st = get_sync_time()
    if st == -1:
        print("get sync time error")
        return -1
    #rawbarcode, date, groupid
    data = get_data_to_add(st[0], st[1])
    if data == 0 or data == -1:
        return -1
    try:
        w1b1 = open_file("engine")
        w2b1 = open_file("OwnedEngine")
    except:
        print("can't open .xlsx files")
        return -1
    try:
        w1s1 = w1b1["engineDB"]
        w1s2 = w1b1["engineGroup"]
        w1s3 = w1b1["syncTime"]
        w2s1 = w2b1["en"]
        glist = []
        for i in data:
            id = (i[0].value)[6:12]
            mip = (i[0].value)[12:]
            type = get_type(mip)
            day = i[1].value
            gid = str(i[2].value)
            if gid not in glist:
                glist.append(gid)
            # 엔진시리얼번호, mip, mip_type, 입고일, 포장일, 출고일, 출고설명, 그룹ID, 불량엔진bool타입, 비고
            #print([id, mip, type, day, day, "", "", gid, 0, ""])
            w1s1.append([id, mip, type, day, day, "", "", gid, 0, ""])
            # 엔진시리얼번호, mip, mip_type, 입고일, 포장일, 그룹ID, 불량엔진, 비고
            w2s1.append([id, mip, type, day, day, gid, 0, ""])
        for i in glist:
            #gio, location
            w1s2.append([i, ""])
        tm = datetime.datetime.now()
        #print(tm.strftime("%Y%m%d"), (tm.strftime("%X"))[0:2] + (tm.strftime("%X"))[3:5] + (tm.strftime("%X"))[6:8])
        w1s3.cell(row=1, column=1).value = tm.strftime("%Y%m%d")
        w1s3.cell(row=1, column=2).value = ((tm.strftime("%X"))[0:2] + (tm.strftime("%X"))[3:5] + (tm.strftime("%X"))[6:8])
        try:
            w1b1.save(get_path("engine"))
            w1b1.close()
            w2b1.save(get_path("OwnedEngine"))
            w2b1.close()
        except:
            print("save error")
            return -1
    except:
        print("can't write in sheets")
        return -1


def select_all_for_report(day):
    dl = defaultdict(list)
    rs = open_sheet("engine", "engineDB")
    for row in list(rs.rows)[1:]:
        # 아직 출고되지않았거나, 기간(a~b)에서 a날짜 이후의 데이터들에 대해 mip, 입고일, 출고일을 리스트에 append
        if (row[5].value == "") or (row[5].value is None) or (int(row[5].value) >= int(day)):
            dl[row[2].value].append([row[1].value, row[3].value, row[5].value])
        # print(row[5].value," ", int(day))
        # 역순 후 마지막행 제외
    return dl


# 보유 엔진에서 해당엔진삭제, 엔진데이터에서 출고일 수정 + 출고설명추가
def delete_row(en, comment, day):
    if (en is None) or (en == ""):
        print("empty en")
    wb1 = open_sheet("engine")
    ws1 = wb1['engineDB']
    wb2 = open_file("OwnedEngine")
    ws2 = wb2['en']
    # check for debug
    c1 = 0
    c2 = 0
    # eid 비교 후 같으면 해당 행 수정. 1부터 시작
    for r in range(1, ws1.max_row + 1):
        if str(ws1.cell(row=r, column=1).value) == en:
            ws1.cell(r, 6).value = day
            ws1.cell(r, 7).value = comment
            c1 = 1
            break
    # eid비교 후 같으면 해당 행 삭제.
    for r in range(1, ws2.max_row + 1):
        if str(ws2.cell(row=r, column=1).value) == en:
            ws2.delete_rows(r)
            c2 = 1
            break
    if (c1 * c2) == 0:
        print("not exist engine")
    wb1.save(get_path("engine"))
    wb1.close()
    wb2.save(get_path("OwnedEngine"))
    wb2.close()
    return 1


'''
def get_excellist():
    rs = open_sheet("engine", "engineDB")
    excelList = []
    tmpList = []
    for x in range(2, rs.max_row + 1):
        for y in range(1, rs.max_column + 1):
            cell = rs.cell(row=x, column=y).value
            if(y == 7):
                continue
            if cell is None:# or math.isnan(rs.cell(row=x, column=y).value):
                tmpList.append('')
            else:
                tmpList.append(cell)
        if tmpList[6] == '': #np.isnan
            tmpList.insert(7, '')
        else:
            #str = get_location(tmpList[6])
            if type(tmpList[6]) == type(int):
                str = get_location(tmpList[6])
            else:
                str = get_location(int(tmpList[6]))
            tmpList.insert(7, str)
        tmpList[0], tmpList[2] = tmpList[2], tmpList[0]
        excelList.append(tmpList)
        tmpList = []
    #excelList = excelList[1:]
    return excelList
'''

#기종, MIP, ENGINE, 입고일, 포장일, 출고일, 출고exp, GROUP, 위치, 불량엔진, 비고
def get_excellist():
    rs = open_sheet("engine", "engineDB")
    tmpList = []
    groupData, locData = get_location()
    first = 0
    for row in rs.rows:
        if first == 0:
            first = 1
            continue

        if row[7].value == '' or row[7].value == None:
            loc = ''
        else:
            if type(row[7]) == type(int):
                idx = groupData.index(row[7].value)
                loc = locData[idx]
            else:
                idx = groupData.index(int(row[7].value))
                loc = locData[idx]

        tmpList.append([
            row[2].value,
            row[1].value,
            row[0].value,
            row[3].value,
            row[4].value,
            row[5].value,
            row[6].value,
            row[7].value,
            loc,
            row[8].value,
            row[9].value
        ])

    for i in range(0, len(tmpList)):
        for j in range(0, len(tmpList[0])):
            if tmpList[i][j] is None:
                tmpList[i][j] = ''
    return tmpList

def get_location():
    rs = pd.read_excel("./DB/engine.xlsx", sheet_name="engineGroup")
    rscolumn = rs[['groupID', 'Location']]
    gList = rscolumn['groupID'].to_list()
    locList = rscolumn['Location'].to_list()
    return gList, locList;


def add_MIP(mip, types):
    wb1 = open_file("engine")
    _ = wb1.active
    ws1 = wb1["types"]
    ws1.append([mip,types])
    ws1.cell(ws1.max_row, 1).alignment = op.styles.Alignment(horizontal="center", vertical="center")
    ws1.cell(ws1.max_row, 2).alignment = op.styles.Alignment(horizontal="center", vertical="center")
    wb1.save(get_path("engine"))
    wb1.close()
    return


def set_invalid_engine(eng, exp):
    wb1 = open_file("engine")
    _ = wb1.active
    ws1 = wb1["engineDB"]

    #elist: 엔진 리스트
    #errorList: 입력으로 받은 값 중 잘못된 엔진 리스트
    elist = []
    errorList = []
    for row in ws1:
        elist.append(row[0].value)
    elist = elist[1:]
    for i in range(0, len(eng)):
        if not eng[i].isdigit():
            errorList.append(eng[i])
            continue
        int_value = int(eng[i])
        str_value = eng[i]
        if int_value in elist:
            idx = elist.index(int_value)
            ws1.cell(row=idx + 2, column=9, value=1)
            ws1.cell(row=idx + 2, column=10, value=exp[i])
        elif str_value in elist:
            idx = elist.index(str_value)
            ws1.cell(row=idx + 2, column=9, value=1)
            ws1.cell(row=idx + 2, column=10, value=exp[i])
        else:
            errorList.append(eng[i])
    wb1.save(get_path("engine"))
    wb1.close()
    return errorList