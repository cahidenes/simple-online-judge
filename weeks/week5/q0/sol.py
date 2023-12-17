camel = input()

for c in camel:
    if c.isupper():
        print("_", end="")
    print(c.lower(),end='')
