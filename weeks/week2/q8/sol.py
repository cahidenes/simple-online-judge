a = int(input())

k = 1
while k < a:
    k *= 2

kuvvetler = []
while k > 0:
    if a >= k:
        kuvvetler.append(k)
        a -= k
    k //= 2

print(*reversed(kuvvetler), sep=" + ")

