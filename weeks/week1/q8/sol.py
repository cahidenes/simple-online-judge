n = int(input())
def f(n):
    if n == 0:
        return 0
    else:
        k = f(n-1) - n
        if k > 0:
            return k
        return f(n-1) + n

print(f(n))
