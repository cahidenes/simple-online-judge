n = int(input())

def asal(x):
    if x == 1:
        return False
    elif x == 2:
        return True
    else:
        for i in range(2, x):
            if x % i == 0:
                return False
        return True

for i in range(2, n):
    if asal(i):
        print(i)
