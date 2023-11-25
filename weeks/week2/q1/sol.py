toplam = 0
say = 0
while True:
    a = int(input())
    if a == 0:
        break
    toplam += a
    say += 1

print(round(toplam/say, 2))
