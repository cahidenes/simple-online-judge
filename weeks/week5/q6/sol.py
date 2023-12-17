n, m = [int(x) for x in input().split()]
baslik = [x.center(10) for x in input().split()]

print('-'*(11*n+1))
print("|", end='')
print(*baslik, sep='|', end='|\n')
print('-'*(11*n+1))
for i in range(m):
    print("|", end='')
    satir = [x.center(10) for x in input().split()]
    print(*satir, sep='|', end='|\n')
    print('-'*(11*n+1))
