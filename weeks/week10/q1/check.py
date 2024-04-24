from tmpcode import Saat
import random

for _ in range(100):
    s1 = random.randint(0, 23)
    d1 = random.randint(0, 59)
    s2 = random.randint(0, 23)
    d2 = random.randint(0, 59)
    d3 = d1 + d2
    if d3 >= 60:
        d3 -= 60
        s3 = 1
    s3 += s1 + s2
    if s3 >= 24:
        s3 -= 24

    saat1 = Saat(saat=s1, dakika=d1)
    saat2 = Saat(saat=s2, dakika=d2)
    if str(saat1 + saat2) != f'{s3:02}:{d3:02}':
        print('print deyince yanlış çıktı:\nBeklenen: ', f'{s3:02}:{d3:02}', '\nÇıktı: ', saat1+saat2)
        exit(1)

    saat3 = Saat(saat=s3, dakika=d3)
    if saat1 + saat2 != saat3:
        print('İşlem hatası:', saat1, '+', saat2, '==', saat3, 'yanlış diyor')
        exit(1)

    if saat1 + saat1 != saat1 * 2:
        print('İşlem hatası:', saat1, '+', saat1, '==', saat1 * 2, 'yanlış diyor')
        exit(1)

exit(0)

