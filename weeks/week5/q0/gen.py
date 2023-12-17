import random
kelimeler = ['bu', 'bir', 'kelime', 'liste', 'center', 'init', 'void', 'print', 'debug']

print(random.choice(kelimeler), end='')
for _ in range(random.randint(1, 4)):
    print(random.choice(kelimeler).capitalize(), end='')
