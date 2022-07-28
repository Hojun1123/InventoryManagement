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


def appendrawbarcode(data):
    wb = openfile("barcode")
    _ = wb.active
    ws = wb["rawBarcode"]
    ws.append(data)
    wb.save(getpath("barcode"))
    wb.close()


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



