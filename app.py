from flask import Flask
from flask import request, render_template, redirect
import dbController as dc
import main.convertRawDataToList as crl
import main.makeReportTable as mrt
import datetime
# Flask 객체 생성
app = Flask(__name__)


# 데코레이션 테스트
@app.route('/test')
def test():
    return render_template("./main/main.html")


# 인덱스 페이지
@app.route('/')
def index():  # put application's code here
    return render_template("./main/login.html")


# 입고(바코드 입력 페이지)
@app.route('/inputrawbarcodestring')
def input_raw_barcode_string():  # put application's code here
    data = dc.get_all_recent_raw_barcodes()
    return render_template("./main/readBarcodeString.html", data=data)


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
            groupid = dc.set_groupid()
            # time부분 나중에 함수로 빼기
            tm = datetime.datetime.now()
            dc.append_raw_barcodes(blist, tm.strftime("%Y%m%d"), tm.strftime("%X"))
        #최근순으로 모든 raw바코드열 가져오기
        data = dc.get_all_recent_raw_barcodes()
        return render_template("./main/readBarcodeString.html")


# 보유 엔진 보고서
@app.route('/holdingengines')
def holding_engines_report():
    #1. 열의 크기는 날짜의 리스트로 동적구현되야함
    #1-2. 월아래에 날짜의 리스트로 보여지는 형식, or 7/27 7/28 ...
    #1-3. 모든 셀의 값은 날짜별로 동적구현되어야함
    #2. 행은
    #3. 맨위 또는 맨아래에 총 MIP에 대해 입고/불출/재고의 합이 출력되어야함
    dates = ["20220729", "20220730", "20220731", "20220801", "20220802", "20220803"]
    table = mrt.make(dc.select_all_for_report(dates[0]), dates)
    return render_template("./main/holdingEnginesReport.html", table=table)


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