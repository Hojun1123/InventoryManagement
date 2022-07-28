from flask import Flask
from flask import request, render_template, redirect
import dbController as dc
import datetime
# Flask 객체 생성
app = Flask(__name__)


# 데코레이션 테스트
@app.route('/test')
def test():
    return "test print"


# 인덱스 페이지
@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


# 입고(바코드 입력 페이지)
@app.route('/inputrawbarcodestring')
def inputrawbarcodestring():  # put application's code here
    data = dc.getallrecentrawbarcodes()
    return render_template("./main/inputRawBarcodeString.html", data=data)


# 바코드 읽기
@app.route('/readBarcode', methods=['GET', 'POST'])
def readbarcode():
    if request.method == 'GET':
        # GET으로 들어올때
        data = dc.getallrecentrawbarcodes()
        return render_template("./main/inputRawBarcodeString.html", data=data)
    else:
        # GET이 아닌 request
        rawBarcodeData = request.form.get("barcode")
        #locationData = request.form.get("location")
        if rawBarcodeData != "":
            tm = datetime.datetime.now()
            # time부분 나중에 함수로 빼기
            dc.appendrawbarcode([rawBarcodeData[6:12], rawBarcodeData, tm.strftime("%Y%m%d"), tm.strftime("%X")])
        data = dc.getallrecentrawbarcodes()
        return render_template("./main/inputRawBarcodeString.html", data=data)


# flask 구동 (main)
if __name__ == '__main__':
    # hp 지정
    # app.run(host="127.0.0.1", port=5000, debug=True)
    # 49.174.54.239:9375
    #
    app.run(host='0.0.0.0', debug=True)