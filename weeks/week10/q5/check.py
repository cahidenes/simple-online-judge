from tmpcode import Araba

araba = Araba('Togg')
if araba.marka != 'Togg':
    print('Arabanın markası doğru değil')
    exit(1)

if araba.teker_sayisi != 4:
    print('Teker sayısı doğru değil')
    exit(1)

if araba.git() != 'gittim':
    print('Git fonksiyonu doğru değil')
    exit(1)

from tmpcode import YarisArabasi

yaris = YarisArabasi('Ferrari')
if yaris.marka != 'Ferrari':
    print("Yarış arabasının markası doğru değil")
    exit(1)

if yaris.teker_sayisi != 4:
    print("Yarıs arabasının teker sayısı doğru değil")
    exit(1)

if yaris.benzin != 5:
    print("Yarış arabasının benzini doğru değil")
    exit(1)

if yaris.git() != "gittim":
    print("Yarış arabası git fonksiyonu inherit ettiği class'ın fonksionunu döndürmüyor")
    exit(1)

if yaris.benzin != 4:
    print("yarış arabası benzini azaltmıyor")
    exit(1)

from tmpcode import Tir

tir = Tir('Tesla')
if tir.marka != 'Tesla':
    print("Tırın markası doğru değil")
    exit(1)

if tir.teker_sayisi != 8:
    print("Tırın teker sayısı doğru değil")
    exit(1)

if tir.yuk != False:
    print("Tırık yük durumu doğru değil")

tir.yukle()

if tir.yuk != True:
    print("Tırık yük durumu doğru değil")

