def ayir(islem, operator):
    parantez = 0
    for i in range(len(islem)):
        if islem[i] == '(':
            parantez += 1
        elif islem[i] == ')':
            parantez -= 1
        elif islem[i] == operator and parantez == 0:
            return i
    return -1

def solve(islem):
    if len(islem) == 1:
        return int(islem[0])
    i = ayir(islem, '+')
    if i != -1:
        return solve(islem[:i]) + solve(islem[i+1:])
    i = ayir(islem, '*')
    if i != -1:
        return solve(islem[:i]) * solve(islem[i+1:])
    return solve(islem[1:-1])

e = input().replace('+', ' + ').replace('*', ' * ').replace('(', ' ( ').replace(')', ' ) ').split()
print(solve(e))
