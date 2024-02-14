olasilik = 0

ayak = input()
if ayak == 'sag':
    olasilik += 1322*100/1653
else:
    olasilik += 388*100/480

kuvvet = input()
if kuvvet == 'dusuk':
    olasilik += 47
elif kuvvet == 'orta':
    olasilik += 81
else:
    olasilik += 63

lig = input()
if lig == 'bundesliga':
    olasilik += 83.33
else:
    olasilik += 73.23

durum = input()
if durum == 'oyun_ici':
    olasilik += 85
else:
    olasilik += 76

olasilik /= 4

print(round(olasilik, 2))
