import random
kelimeler = ['bir', 'kalem', 've', 'defter', 'kitap', 'masa', 'bilgisayar', 'python', 'kasa', 'kedi']

for i in range(random.randint(100, 1000)):
    print(random.choice(kelimeler), end=' ')
