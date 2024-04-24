from tmpcode import Saat
import random

for _ in range(100):
    s = random.randint(0, 23)
    d = random.randint(0, 59)

    saat = Saat(saat=s, dakika=d)
    if str(saat) != f'{s:02}:{d:02}':
        print('print deyince yanlış çıktı:\nBeklenen: ', f'{s:02}:{d:02}', '\nÇıktı: ', saat)
        exit(1)

    saat = Saat(saat=s)
    if str(saat) != f'{s:02}:00':
        print('print deyince yanlış çıktı:\nBeklenen: ', f'{s:02}:00', '\nÇıktı: ', saat)
        exit(1)

    saat = Saat(dakika=d)
    if str(saat) != f'00:{d:02}':
        print('print deyince yanlış çıktı:\nBeklenen: ', f'00:{d:02}', '\nÇıktı: ', saat)
        exit(1)

exit(0)

