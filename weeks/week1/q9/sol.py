mt1 = int(input())
mt2 = int(input())
curve = int(input())

sayim = (curve + 20 - mt1*0.3 - mt2*0.3)/0.4
if sayim > 100:
    print('AA: imkansiz')
elif sayim < 0:
    print('AA: 0')
else:
    print('AA:', round(sayim, 2))

sayim = (curve + 15 - mt1*0.3 - mt2*0.3)/0.4
if sayim > 100:
    print('BA: imkansiz')
elif sayim < 0:
    print('BA: 0')
else:
    print('BA:', round(sayim, 2))

sayim = (curve + 10 - mt1*0.3 - mt2*0.3)/0.4
if sayim > 100:
    print('BB: imkansiz')
elif sayim < 0:
    print('BB: 0')
else:
    print('BB:', round(sayim, 2))

sayim = (curve + 5 - mt1*0.3 - mt2*0.3)/0.4
if sayim > 100:
    print('CB: imkansiz')
elif sayim < 0:
    print('CB: 0')
else:
    print('CB:', round(sayim, 2))

sayim = (curve - mt1*0.3 - mt2*0.3)/0.4
if sayim > 100:
    print('CC: imkansiz')
elif sayim < 0:
    print('CC: 0')
else:
    print('CC:', round(sayim, 2))

sayim = (curve - 5 - mt1*0.3 - mt2*0.3)/0.4
if sayim > 100:
    print('DC: imkansiz')
elif sayim < 0:
    print('DC: 0')
else:
    print('DC:', round(sayim, 2))

sayim = (curve - 10 - mt1*0.3 - mt2*0.3)/0.4
if sayim > 100:
    print('DD: imkansiz')
elif sayim < 0:
    print('DD: 0')
else:
    print('DD:', round(sayim, 2))
