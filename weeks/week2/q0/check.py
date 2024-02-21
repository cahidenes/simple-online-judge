import os
import random
os.system('rm -f yeni.txt')
random_text = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 10))
open('yazi.txt', 'w').write(random_text)
import tmpcode
try:
    yeni = open('yeni.txt').read()
except:
    print('yeni.txt bulunamadı')
    exit(1)
if yeni == random_text:
    exit(0)
else:
    print('yeni.txt içeriği yanlış')
    exit(1)

