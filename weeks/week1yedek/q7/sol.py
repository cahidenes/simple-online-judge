not1 = input()
kredi1 = int(input())
not2 = input()
kredi2 = int(input())
not3 = input()
kredi3 = int(input())
not4 = input()
kredi4 = int(input())
not5 = input()
kredi5 = int(input())

if not1 == 'AA':
    not1 = 4.0
elif not1 == 'BA':
    not1 = 3.5
elif not1 == 'BB':
    not1 = 3.0
elif not1 == 'CB':
    not1 = 2.5
elif not1 == 'CC':
    not1 = 2.0
elif not1 == 'DC':
    not1 = 1.5
elif not1 == 'DD':
    not1 = 1.0
elif not1 == 'F':
    not1 = 0.0

if not2 == 'AA':
    not2 = 4.0
elif not2 == 'BA':
    not2 = 3.5
elif not2 == 'BB':
    not2 = 3.0
elif not2 == 'CB':
    not2 = 2.5
elif not2 == 'CC':
    not2 = 2.0
elif not2 == 'DC':
    not2 = 1.5
elif not2 == 'DD':
    not2 = 1.0
elif not2 == 'F':
    not2 = 0.0

if not3 == 'AA':
    not3 = 4.0
elif not3 == 'BA':
    not3 = 3.5
elif not3 == 'BB':
    not3 = 3.0
elif not3 == 'CB':
    not3 = 2.5
elif not3 == 'CC':
    not3 = 2.0
elif not3 == 'DC':
    not3 = 1.5
elif not3 == 'DD':
    not3 = 1.0
elif not3 == 'F':
    not3 = 0.0

if not4 == 'AA':
    not4 = 4.0
elif not4 == 'BA':
    not4 = 3.5
elif not4 == 'BB':
    not4 = 3.0
elif not4 == 'CB':
    not4 = 2.5
elif not4 == 'CC':
    not4 = 2.0
elif not4 == 'DC':
    not4 = 1.5
elif not4 == 'DD':
    not4 = 1.0
elif not4 == 'F':
    not4 = 0.0

if not5 == 'AA':
    not5 = 4.0
elif not5 == 'BA':
    not5 = 3.5
elif not5 == 'BB':
    not5 = 3.0
elif not5 == 'CB':
    not5 = 2.5
elif not5 == 'CC':
    not5 = 2.0
elif not5 == 'DC':
    not5 = 1.5
elif not5 == 'DD':
    not5 = 1.0
elif not5 == 'F':
    not5 = 0.0

notun = (not1*kredi1 + not2*kredi2 + not3*kredi3 + not4*kredi4 + not5*kredi5) / (kredi1 + kredi2 + kredi3 + kredi4 + kredi5)
print(round(notun, 2))
if notun >= 2:
    print("geçtiniz")
else:
    print("kaldınız")
