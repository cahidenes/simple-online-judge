kelimeler = [x.capitalize() for x in input().split()]
kelimeler.sort(reverse=True)
print(*kelimeler)
