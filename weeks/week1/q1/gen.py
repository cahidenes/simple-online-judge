import random
def exp(maxdepth):
    if maxdepth == 0:
        return str(random.randint(1, 50))
    if random.random() < 0.3:
        return str(random.randint(1, 50))
    elif random.random() < 0.3:
        return "(" + exp(maxdepth-1) + ")"
    elif random.random() < 0.33:
        return exp(maxdepth-1) + "+" + exp(maxdepth-1)
    elif random.random() < 0.5:
        return exp(maxdepth-1) + "-" + exp(maxdepth-1)
    else:
        return exp(maxdepth-1) + "*" + exp(maxdepth-1)

print(exp(20))
