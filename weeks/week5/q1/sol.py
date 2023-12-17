fr = input()

name = fr.split()[1]
print(name)

rangeler = fr[fr.index('(')+1:fr.index(')')].split(',')
if len(rangeler) == 1:
    print(0)
    print(int(rangeler[0].strip()))
    print(1)
elif len(rangeler) == 2:
    print(int(rangeler[0].strip()))
    print(int(rangeler[1].strip()))
    print(1)
else:
    print(int(rangeler[0].strip()))
    print(int(rangeler[1].strip()))
    print(int(rangeler[2].strip()))
