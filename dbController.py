#db control
import openpyxl as op


def opensheet(file, sheet):
    rb = op.load_workbook("./DB/"+file+".xlsx")
    return rb[sheet]


def openfile(file):
    return op.load_workbook("./DB/" + file + ".xlsx")


def getpath(file):
    return "./DB/" + file + ".xlsx"


# userController
def getuserpw(id):
    rs = opensheet("user", "user")

    #행단위로 읽어와 해당 id의 pw를 반환.
    for row in rs.rows:
        if row[0].value == id:
            print("get pw:", row[1].value, " of "+id)
            return row[1].value
    return "None"

#print(getuserpw("admin"))


# barcodeController
def getallrecentrawbarcodes():
    rs = opensheet("barcode", "rawBarcode")
    dl = []
    #가장 최근 추가한것이 맨위로.
    rr = rs.rows
    #dl.append(["번호", "바코드", "time"])
    for row in reversed(list(rr)):
        #bid, rawBarcodeString, date, time
        dl.append([row[0].value, row[1].value, row[2].value, row[3].value])
    #역순 후 마지막행 제외
    dl.pop()
    return dl


def appendrawbarcodes(data, day, time):
    wb1 = openfile("barcode")
    _ = wb1.active
    w1s1 = wb1["rawBarcode"]

    wb2 = openfile("engine")
    __ = wb2.active
    w2s1 = wb2["engineDB"]
    w2s2 = wb2["engineGroup"]

    _ = 0
    gi = setgroupid()
    for i in data:
        _ += 1
        gi += _
        #gk, location
        w2s2.append([str(gi), ""])
        for j in i:
            # 엔진시리얼번호, 바코드, 날짜, 시간, 그룹ID
            w1s1.append([j[6:12], j, day, time, str(gi)])
            # 엔진시리얼번호, mip, mip_type, 입고일, 포장일, 출고일, 출고설명, 그룹ID, 불량엔진bool타입, 비고
            w2s1.append([j[6:12], j[12:], gettype(j[12:]), day, day, "", "", str(gi), 0, ""])
    wb1.save(getpath("barcode"))
    wb1.close()
    wb2.save(getpath("engine"))
    wb2.close()


def setgroupid():
    wb = opensheet("barcode", "rawBarcode")
    length = len(list(wb.rows))
    return 10000+length


# engineController


def gettype(mip):
    rs = opensheet("engine", "types")
    for row in rs.rows:
        #empty rows 탐색 제외
        if row[0].value is None:
            break
        if row[0].value == mip:
            return row[1].value
    print("Invalid MIP")
    return -1


