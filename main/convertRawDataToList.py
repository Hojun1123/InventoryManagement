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