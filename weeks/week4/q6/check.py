import random
from tmpcode import tahmin

open('tmperror', 'w').write('girdiye bakınız')
open('tmpexpected', 'w').write('girdiye bakınız')

for _ in range(100):
    inputfile = open('tmpinput', 'w')
    bil = random.randint(1, 1000)
    inputfile.write("tuttuğum sayı: " + str(bil) + "\n")
    inputfile.write(f'tahmin("ilk"): ')
    prompt = "ilk"
    for k in range(20):
        ret = tahmin(prompt)
        inputfile.write(str(ret) + "\n")
        if ret == bil:
            break
        elif ret < bil:
            prompt = "yukarı"
        else:
            prompt = "aşağı"
        if k == 19:
            inputfile.write("deneme hakkın bitti")
        else:
            inputfile.write(f'tahmin("{prompt}"): ')
    else:
        exit(1)
exit(0)
