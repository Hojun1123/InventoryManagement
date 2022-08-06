# db control
import openpyxl as op
from collections import defaultdict

def open_sheet(file, sheet):
    rb = op.load_workbook("./DB/" + file + ".xlsx")
    return rb[sheet]


def open_file(file):
    return op.load_workbook("./DB/" + file + ".xlsx")


def get_path(file):
    return "./DB/" + file + ".xlsx"


# userController
def get_user_pw(id):
    rs = open_sheet("user", "user")

    # 행단위로 읽어와 해당 id의 pw를 반환.
    for row in rs.rows:
        if row[0].value == id:
            print("get pw:", row[1].value, " of " + id)
            return row[1].value
    return "None"


# print(getuserpw("admin"))


# barcodeController
def get_all_recent_raw_barcodes():
    rs = open_sheet("barcode", "rawBarcode")
    dl = []
    # 가장 최근 추가한것이 맨위로.
    rr = rs.rows
    # dl.append(["번호", "바코드", "time"])
    for row in reversed(list(rr)):
        # bid, rawBarcodeString, date, time
        dl.append([row[0].value, row[1].value, row[2].value, row[3].value])
    # 역순 후 마지막행 제외
    dl.pop()
    return dl


def append_raw_barcodes(data, day, time):
    wb1 = open_file("barcode")
    _ = wb1.active
    w1s1 = wb1["rawBarcode"]

    wb2 = open_file("engine")
    __ = wb2.active
    w2s1 = wb2["engineDB"]
    w2s2 = wb2["engineGroup"]

    wb3 = open_file("OwnedEngine")
    ___ = wb3.active
    w3s1 = wb3["en"]

    c = 0
    gi = set_groupid()
    for i in data:
        c += 1
        gi += c
        # gk, location
        w2s2.append([str(gi), ""])
        for j in i:
            # 엔진시리얼번호, 바코드, 날짜, 시간, 그룹ID
            w1s1.append([j[6:12], j, day, time, str(gi)])
            # 엔진시리얼번호, mip, mip_type, 입고일, 포장일, 출고일, 출고설명, 그룹ID, 불량엔진bool타입, 비고
            w2s1.append([j[6:12], j[12:], get_type(j[12:]), day, day, "", "", str(gi), 0, ""])
            # 엔진시리얼번호, mip, mip_type, 입고일, 포장일, 그룹ID, 불량엔진, 비고
            w3s1.append([j[6:12], j[12:], get_type(j[12:]), day, day, str(gi), 0, ""])
    wb1.save(get_path("barcode"))
    wb1.close()
    wb2.save(get_path("engine"))
    wb2.close()
    wb3.save(get_path("OwnedEngine"))
    wb3.close()


def set_groupid():
    wb = open_sheet("barcode", "rawBarcode")
    length = len(list(wb.rows))
    return 10000 + length


# engineController
def select_all_for_report(day):
    dl = defaultdict(list)
    rs = open_sheet("engine", "engineDB")
    for row in list(rs.rows)[1:]:
        # 아직 출고되지않았거나, 기간(a~b)에서 a날짜 이후의 데이터들에 대해 mip, 입고일, 출고일을 추가
        if (row[5].value == "") or (row[5].value is None) or (int(row[5].value) >= int(day)):
            dl[row[2].value].append([row[1].value, row[3].value, row[5].value])
        #print(row[5].value," ", int(day))
        # 역순 후 마지막행 제외
    return dl


def get_type(mip):
    rs = open_sheet("engine", "types")
    for row in rs.rows:
        # empty rows 탐색 제외
        if row[0].value is None:
            break
        if row[0].value == mip:
            return row[1].value
    print("Invalid MIP")
    return -1


def select_engine_by_mip(mip):
    # types시트에서 없는 mip가 들어올경우에 대해 처리하는 부분 추가(일단 보류)
    if (mip is None) or mip == "":
        print("empty MIP")
        return -1
    # mip가 일치하는 엔진들을 모두 list로 반환
    result = []
    rs = open_sheet("OwnedEngine", "en")
    for row in rs.rows:
        if row[1].value == mip:
            result.append(row)
    return result


#해당 날짜에 입고된 mip 엔진리스트를 반환
def select_input_engine_by_mip_with_day(mip, day):
    if (mip is None) or mip == "":
        print("empty MIP")
        return -1
    if (day is None) or day == "":
        print("empty day")
        return -1
    rs = open_sheet("engine", "engineDB")
    result = []
    for row in rs.rows:
        if (row[1].value == mip) and (str(row[3].value) == day):
            result.append(row)
    return result


#해당 날짜에 출고된 mip 엔진리스트를 반환
def select_output_engine_by_mip_with_day(mip, day):
    if (mip is None) or mip == "":
        print("empty MIP")
        return -1
    if (day is None) or day == "":
        print("empty day")
        return -1
    rs = open_sheet("engine", "engineDB")
    result = []
    for row in rs.rows:
        if (row[1].value == mip) and (str(row[5].value) == day):
            result.append(row)
    return result


#보유 엔진에서 해당엔진삭제, 엔진데이터에서 출고일 수정 + 출고설명추가
def delete_row(en, comment, day):
    if (en is None) or (en == ""):
        print("empty en")

    wb1 = open_file("engine")
    _ = wb1.active
    ws1 = wb1['engineDB']

    wb2 = open_file("OwnedEngine")
    __ = wb2.active
    ws2 = wb2['en']

    #check for debug
    c1 = 0
    c2 = 0

    #eid 비교 후 같으면 해당 행 수정. 1부터 시작
    for r in range(1, ws1.max_row+1):
        if str(ws1.cell(row=r, column=1).value) == en:
            ws1.cell(r, 6).value = day
            ws1.cell(r, 7).value = comment
            c1 = 1
            break

    #eid비교 후 같으면 해당 행 삭제.
    for r in range(1, ws2.max_row+1):
        if str(ws2.cell(row=r, column=1).value) == en:
            ws2.delete_rows(r)
            c2 = 1
            break

    if (c1*c2) == 0:
        print("not exist engine")

    wb1.save(get_path("engine"))
    wb1.close()
    wb2.save(get_path("OwnedEngine"))
    wb2.close()

    return 1

