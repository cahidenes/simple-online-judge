import datetime

monthdic = {
        "Ocak": 1,
        "Şubat": 2,
        "Mart": 3,
        "Nisan": 4,
        "Mayıs": 5,
        "Haziran": 6,
        "Temmuz": 7,
        "Ağustos": 8,
        "Eylül": 9,
        "Ekim": 10,
        "Kasım": 11,
        "Aralık": 12
        }

weekdic = {
        "Pazartesi": 0,
        "Salı": 1,
        "Çarşamba": 2,
        "Perşembe": 3,
        "Cuma": 4,
        "Cumartesi": 5,
        "Pazar": 6
           }
day, month, week = input().split()
day = int(day)
month = monthdic[month]
week = weekdic[week]

for yil in range(2014, 2024):
    bugun = datetime.date(yil, month, day)
    if bugun.weekday() == week:
        print(yil)
        break

