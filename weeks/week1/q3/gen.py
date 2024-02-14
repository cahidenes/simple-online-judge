import random

n = random.randint(3, 8)
m = random.randint(5, 15)
print(n, m)
print(*random.sample(['Boy', 'Genişlik', 'En', 'Kalınlık', 'Yaş', 'Sağlık', 'Verimlilik', 'Yararlılık', 'Mesafe', 'Yaşam', 'Derinlik', 'Yoğunluk'], n))
for i in range(m):
    print(*[random.randint(1, 10000) for _ in range(n)])

