import random
print(random.randint(1, 28), end=' ')
aylar = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
hafta = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', "Pazar"]
print(random.choice(aylar), end=' ')
print(random.choice(hafta))
