a = int(input())
b = int(input())

if a > b and a % 2 == 0 and b % 2 == 1:
    print('uyumlu')
elif a < b and a % 3 == 0 and b - a >= 10:
    print('uyumlu')
elif a == b and a > 50:
    print('uyumlu')
else:
    print('uyumsuz')

