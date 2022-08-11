from flask import Flask
from flask import request, render_template, redirect, flash
from math import ceil
import dbController as dc
import main.convertRawDataToList as crl
import main.makeReportTable as mrt
import main.getDateList as gdl
import datetime
# Flask 객체 생성
app = Flask(__name__)
app.config["SECRET_KEY"] = "sh291hfwnh8@hwqjh2(*@#*Uh2N2920hF@H0Fh@C293"
'''
# 데코레이션 테스트
@app.route('/inventory')
def inventory():
    return render_template("./main/inventory.html")
'''


@app.route('/main')
def main_page():
    return render_template("./main/main.html")

@app.route('/inventory')
def inventory():
    excelList = dc.get_excellist()
    length = len(excelList)
    return render_template("./main/inventory.html", excelList = excelList, length = length)


# 인덱스 페이지
@app.route('/')
def index():  # put application's code here
    return render_template("./main/login.html")

# 바코드 읽기
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
            tm = datetime.datetime.now()
            dc.append_raw_barcodes(blist, tm.strftime("%Y%m%d"), tm.strftime("%X"))
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
            print(blist)
            for b in blist:
                print(b)
                dc.delete_row(b, "comment test", tm.strftime("%Y%m%d"))
        return render_template("./main/releaseEngine.html")


# 보유 엔진 보고서
@app.route('/holdingengines')
def holding_engines_report():
    #test dates
    dates = gdl.datelist("20220725", "20220805")
    table = mrt.make(dc.select_all_for_report(dates[0]), dates)
    return render_template("./main/holdingEnginesReport.html", table=table)

# mip 추가
@app.route('/addMIP', methods=['GET', 'POST'])
def add_MIP_type():
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

# flask 구동 (main)
if __name__ == '__main__':
    # hp 지정
    # app.run(host="127.0.0.1", port=5000, debug=True)
    # 49.174.54.239:9375
    #
    app.run(host='0.0.0.0', debug=True)


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