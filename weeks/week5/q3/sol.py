sayilar = [int(x) for x in input().split()]
geldi = set()
for i in sayilar:
    if i in geldi:
        print('var')
    else:
        print('yok')
    geldi.add(i)
