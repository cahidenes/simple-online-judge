import cowsay

karakter = input()
if karakter in cowsay.char_names:
    cowsay.chars[karakter]('SA, Python çok güzel')
else:
    print('YOK')
