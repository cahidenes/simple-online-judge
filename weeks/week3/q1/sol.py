def alan(a, b=None):
    if b:
        return a*b, 2*(a+b)
    else:
        return a*a, 4*a
