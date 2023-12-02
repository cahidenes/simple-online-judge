e = input()
e = e.replace('+', ' + ')
e = e.replace('*', ' * ')
e = e.replace('(', ' ( ')
e = e.replace(')', ' ) ')
e = e.split()

def solve(islem):
    if len(islem) == 1:
        return int(islem[0])

    parantez = 0
    for i in range(len(islem)):
        if islem[i] == '(':
            parantez += 1
        elif islem[i] == ')':
            parantez -= 1
        elif islem[i] == '+' and parantez == 0:
            return solve(islem[:i]) + solve(islem[i+1:])

    parantez = 0
    for i in range(len(islem)):
        if islem[i] == '(':
            parantez += 1
        elif islem[i] == ')':
            parantez -= 1
        elif islem[i] == '*' and parantez == 0:
            return solve(islem[:i]) * solve(islem[i+1:])

    return solve(islem[1:-1])


print(solve(e))

