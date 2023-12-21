sifre = input()

alfabe =      'abcdefghijklmnopqrstuvwxyz'
permutasyon = 'dcfxtpvmkesgbjoaluywizhqnr'

def karistir(c, adim=3):
    if adim == 0 or c not in alfabe:
        return c
    return karistir(permutasyon[alfabe.index(c)], adim-1)

for c in sifre:
    print(karistir(c), end='')
