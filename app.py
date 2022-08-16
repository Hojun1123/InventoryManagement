from flask import Flask
from flask import request, render_template, redirect, flash, session
from math import ceil
import dbController as dc
import main.convertRawDataToList as crl
import main.makeReportTable as mrt
import main.getDateList as gdl
from datetime import datetime
# Flask 객체 생성
app = Flask(__name__)
#flash secret_key
app.config["SECRET_KEY"] = "sh291hfwnh8@hwqjh2(*@#*Uh2N2920hF@H0Fh@C293"
allList = []
testList = []

# 인덱스 페이지
@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    if request.method == 'POST':
        id = request.form.get("id")
        pwd = request.form.get("pwd")

        if id == '' or pwd == '':
            flash("아이디와 비빌번호를 입력해주세요.")
            return render_template("./main/login.html")

        if id == "manager" and pwd == "manager123!@#":
            session['userid'] = "manager"
            flash("관리자님, 안녕하세요!")
            return render_template("./main/login.html")
        elif id == "user" and pwd == "user123!@#":
            session['userid'] = "user"
            flash("사용자님, 안녕하세요!")
            return render_template("./main/login.html")
        else:
            flash("아이디 혹은 비빌번호가 잘못되었습니다.")
            return render_template("./main/login.html")
    else:
        return render_template("./main/login.html")

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid',None)
    return redirect('/')

@app.route('/main')
def main_page():
    return render_template("./main/main.html")

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == "GET":
        excelList = dc.get_excellist()
        global allList
        allList = excelList
        length = len(excelList)
        return render_template("./main/inventory.html", excelList=excelList)
    else:
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        if len(startdate) < 10 or len(enddate) < 10:
            return "<script>alert(\'날짜를 선택해 주세요.\')\nwindow.history.back()</script>"
        sd = str(startdate[0:4] + startdate[5:7] + startdate[8:10])
        ed = str(enddate[0:4] + enddate[5:7] + enddate[8:10])
        data = dc.select_by_date(sd, ed)
        length = len(data)
        return render_template("./main/inventory.html", excelList=data, startdate=str(startdate), enddate=str(enddate))



# 바코드 읽기    #일단 보류
@app.route('/readBarcode', methods=['GET', 'POST'])
def read_barcode():
    if request.method == 'GET':
        return render_template("./main/readBarcodeString.html")
    else:
        # GET이 아닌 request (확인submit)
        rawBarcodeData = request.form.get("barcode")
        if rawBarcodeData != "" and rawBarcodeData is not None:
            blist = crl.convert(rawBarcodeData)
            # time부분 나중에 함수로 빼기
            dc.append_raw_barcodes(blist)
        #최근순으로 모든 raw바코드열 가져오기
        return render_template("./main/readBarcodeString.html")


# 출고 바코드 찍기
@app.route('/releaseEngine', methods=['GET', 'POST'])
def release_engine():
    if request.method == 'GET':
        return render_template("./main/releaseEngine.html")
    else:
        barcodes = request.form.get("barcode")
        if barcodes != "" and barcodes is not None:
            blist = crl.convert2(barcodes)
            tm = datetime.datetime.now()
            for b in blist:
                print(b)
                dc.delete_row(b, "comment test", tm.strftime("%Y%m%d"))
        return render_template("./main/releaseEngine.html")


# 보유 엔진 보고서
@app.route('/report', methods=['GET', 'POST'])
def holding_engines_report():
    #test dates
    if request.method == 'GET':
        return render_template("./main/report.html", table="<p>날짜를 선택해주세요.</p>")
    else:
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        if len(startdate) < 10 or len(enddate) < 10:
            return "<script>alert(\'날짜를 선택해 주세요.\')\nwindow.history.back()</script>"
        sd = str(startdate[0:4] + startdate[5:7] + startdate[8:10])
        ed = str(enddate[0:4] + enddate[5:7] + enddate[8:10])
        dates = gdl.datelist(sd, ed)
        table = mrt.make(dc.select_all_for_report(dates[0]), dates)
        return render_template("./main/report.html", table=table, startdate=str(startdate), enddate=str(enddate))


# dailylist
@app.route('/dailylist')
def daily_engine_list():
    inputList = []
    outputList = []
    today = dc.get_today_date()
    for i in range(0, len(allList)):
        if allList[i][3] == today:
            inputList.append(allList[i])
        elif allList[i][5] == today:
            outputList.append(allList[i])
    inputlen = len(inputList)
    outputlen = len(outputList)
    return render_template("./main/dailylist.html", inputList = inputList, inputlen = inputlen, outputList = outputList, outputlen = outputlen)


# mip 추가
@app.route('/addMIP', methods=['GET', 'POST'])
def add_mip_type():
    if request.method == 'GET':
        return render_template("./main/addMIP.html")
    else:
        mip = request.form.get("mip")
        type = request.form.get("type")
        if mip == "" and mip is None:
            return render_template("./main/addMIP.html")
        if type == "" and type is None:
            return render_template("./main/addMIP.html")
        if len(mip) != 4:
            return render_template("./main/addMIP.html")
        dc.add_MIP(mip, type)
        return render_template("./main/addMIP.html")

#에러엔진 설정
@app.route('/setInvalidEngine', methods=['GET', 'POST'])
def set_invalid_engine_exp():
    errorList = []
    if request.method == 'GET':
        return render_template("./main/setInvalidEngine.html")
    else:
        eng = request.form.getlist("ENG[]")
        exp = request.form.getlist("EXP[]")
        errorList = dc.set_invalid_engine(eng, exp)
        errorEngine = '입력 에러 엔진: '

        if len(errorList) != 0:
            for eng in errorList:
                errorEngine = errorEngine + eng + ' '
            flash(errorEngine)
        return render_template("./main/setInvalidEngine.html", errorList = errorList)


#동기화
@app.route('/refresh')
def refresh():
    dc.synchronization()
    print("동기화 완료")
    return "<script>alert(\'동기화 완료\')\nwindow.history.back()</script>"

@app.route('/inventoryPayment', methods=['GET', 'POST'])
def test():
    global testList, allList
    if request.method == "GET":
        startdate, enddate = datetime.now(), datetime.now()
        startdate, enddate = str(startdate), str(enddate)
        sd = str(startdate[0:4] + startdate[5:7] + startdate[8:10])
        ed = str(enddate[0:4] + enddate[5:7] + enddate[8:10])
        check, paymentList = dc.inventory_payment(testList, allList, sd, ed)
        return render_template("./main/inventoryPayment.html", paymentList=paymentList)
    else:
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        if len(startdate) < 10 or len(enddate) < 10:
            return "<script>alert(\'날짜를 선택해주세요\')\nwindow.history.back()</script>"
        sd = str(startdate[0:4] + startdate[5:7] + startdate[8:10])
        ed = str(enddate[0:4] + enddate[5:7] + enddate[8:10])
        #data = dc.select_by_date(sd, ed)
        data = dc.base_inventory_list(allList, sd, ed)
        check, paymentList = dc.inventory_payment(data, allList, sd, ed)
        print(paymentList)

        if check == False:
            return "<script>alert(\'" + paymentList + "엔진의 Type, MIP 가 DB에 추가되어있지 않습니다." + "\')\nwindow.history.back()</script>"
        elif check == True:
            return render_template("./main/inventoryPayment.html", paymentList=paymentList )
        #dc.inventory_payment(data)
        #dc.base_inventory_list(data, startdate, enddate)
        return render_template("./main/inventoryPayment.html", paymentList=paymentList)
# flask 구동 (main)
if __name__ == '__main__':
    # hp 지정
    # app.run(host="127.0.0.1", port=5000, debug=True)
    # 49.174.54.239:9375
    #
    testList = dc.get_excellist()
    allList = dc.get_excellist()
    app.run(host='0.0.0.0', debug=True, threaded=True)


'''
TEST
G4FMNU259752BE02
G4FMNU259751BE02
G4FMNU259750BE02
G4FMNU259749BE02
G4FDEH408157G20Y
G4FMNU259753BE02
G4FMNU259753BE02
G4FMNU259754BE02
G4FMNU259755BE02
G4FDEH408157G20Y
G4FMNU259757BE02
G4FMNU259758BE02
G4FDEH408157G20Y
'''