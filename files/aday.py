import random

adaylar = []
secim = 0
index = 0

def reset():
    puan_min = random.randint(1, 10000)
    puan_max = random.randint(puan_min+10, 100000)
    adaylar.clear()
    for i in range(100):
        adaylar.append(random.randint(puan_min, puan_max))
    global secim, index
    secim = 0
    index = 0

def adayla_gorus():
    global index, secim
    if index == 99:
        if secim == 0:
            secim = adaylar[index-1]
        return 0
    else:
        index += 1
        return adaylar[index-1]

def kabul_et():
    global index, secim
    if secim == 0 and 0 < index <= 100:
        secim = adaylar[index-1]
