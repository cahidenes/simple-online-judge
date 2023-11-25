l = input().split()
for i in range(len(l)):
    l[i] = int(l[i])
maxkar = 0
for i in range(len(l)):
    for j in range(i+1, len(l)):
        maxkar = max(maxkar, l[i] - l[j])
print(maxkar)
