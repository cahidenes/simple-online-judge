import pyperclip
import random

text = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 10))
open('tmpinput', 'w').write(text)
open('tmpexpected', 'w').write(text+'!')

pyperclip.copy(text)
import tmpcode
output = pyperclip.paste()
open('tmpoutput', 'w').write(output)
if output == text+'!':
    exit(0)
exit(1)
