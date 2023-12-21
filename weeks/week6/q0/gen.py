import random
kelimeler = ['bu', 'bir', 'kelime', 'liste', 'center', 'init', 'void', 'print', 'debug', 'elma', 'armut', 'kalem', 'silgi', 'defter']

print(*random.sample(kelimeler, random.randint(3, 7)))
