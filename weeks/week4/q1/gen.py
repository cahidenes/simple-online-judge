import random
kelimeler = ['ve', 'bir', 'neden', 'nasıl', 'kalem', 'defter', 'kodlama', 'yazılım', 'python', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1den', '2den', '3e', '4ü', '5te']

print(' '.join(random.sample(kelimeler, random.randint(4, 10))))
