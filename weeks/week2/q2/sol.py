l = [1, 1]
a = int(input())
b = int(input())
for i in range(2, 101):
    l.append(l[i-2]*a + l[i-1]*b)

n = int(input())
print(l[n-1])

