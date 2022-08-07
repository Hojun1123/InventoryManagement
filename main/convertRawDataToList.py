def convert(data):
    d = data.replace("\r", "")
    d = d.split("\n")
    result = []
    temp = []
    for i in d:
        #중복인식처리
        if i in temp:
            continue

        #print barcode
        if i == "G4FDEH408157G20Y":
            if len(temp) > 0:
                result.append(temp)
                temp = []
        else:
            temp.append(i)
    return result


def convert2(data):
    d = data.replace("\r", "")
    d = d.split("\n")
    temp = []
    for i in d:
        # 중복인식처리
        if (i in temp) or len(i) != 16:
            continue
        else:
            temp.append(i[6:12])
    return temp

#mip, 기종 길이 체크
def mipConvertCheck(mipData, typeData):
    m = mipData.replace("\r", "")
    m = m.split("\n")
    t = typeData.replace("\r", "")
    t = t.split("\n")

    for i in m:
        if len(i) != 4:
            return False

    if(len(m) == len(t)):
        return True
    return False


def mipConvert(mipData, typeData):
    m = mipData.replace("\r", "")
    m = m.split("\n")
    t = typeData.replace("\r", "")
    t = t.split("\n")
    mipTemp = []
    typeTemp = []
    #mip List생성
    for i in m:
        if i in mipTemp:
            continue
        mipTemp.append(i)

    for i in t:
        if i in typeTemp:
            continue
        typeTemp.append(i)

    return mipTemp, typeTemp