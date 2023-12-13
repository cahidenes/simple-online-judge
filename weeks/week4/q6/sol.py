mx = 1000
mn = 1

def tahmin(sonuc):
    global mn, mx
    orta = (mx+mn)//2
    if sonuc == "ilk":
        mn, mx = 1, 1000
        orta = (mx+mn)//2
        return orta
    elif sonuc == "yukarı":
        mn = orta
        orta = (mx+mn)//2
        return orta
    elif sonuc == "aşağı":
        mx = orta
        orta = (mx+mn)//2
        return orta

