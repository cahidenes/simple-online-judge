import cowsay

karakter = input()
if karakter in cowsay.char_names:
    cowsay.char_funcs[karakter]('SA, Python çok güzel')
else:
    print('YOK')
