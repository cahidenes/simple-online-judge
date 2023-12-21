sifre = input()

d = {'a': '11', 'b': 'E', 'e': '7', 'k': 'B', 'l': 'A', 'm': '9', 'n': 'I', 'o': 'M', 'r': '21', 's': 'K', 't': '4', 'u': 'N', 'y': '8', 'z': 'U'}

alf1 = 'zyxwvutsrqponmlkjihgfedcba'
alf2 = 'abcdefghijklmnopqrstuvwxyz'

for c in sifre:
    try:
        try:
            print(int(d[c])*100, end=' ')
        except ValueError:
            print(alf1.index(c)+30, end=' ')
        except KeyError:
            print(alf2.index(c), end=' ')
    except:
        print(c, end=' ')
