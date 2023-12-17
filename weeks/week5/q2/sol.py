n = int(input())

def bas(s=''):
    if len(s) == n:
        print(s)
        return
    bas(s+'0')
    bas(s+'1')

bas()
