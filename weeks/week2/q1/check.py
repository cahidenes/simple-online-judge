try:
    from tmpcode import bul
except:
    print('bul fonksiyonunu yazmamışsın >:(')
    exit(1)

try:
    if bul('müj____k') != 'müjdelik':
        print('hatalı kelime')
        exit(1)
    if bul('sarma_ık_il_er') != 'sarmaşıkgiller':
        print('hatalı kelime')
        exit(1)
except:
    print('bul fonksiyonunda hata var >:(')
    exit(1)
exit(0)

