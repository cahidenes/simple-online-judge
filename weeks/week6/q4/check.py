import os
soru = 'Halid Ziya Uşaklıgil'
answer = 'Halid Ziya Uşaklıgil (also spelled Halit and Uşakizâde) (Turkish pronunciation: [haːˈlit ziˈjaː uˌʃaklɯˈɟil]; 1866 – 27 March 1945) was a Turkish author, poet, and playwright. A part of the Edebiyat-ı Cedide ("New Literature") movement of the late Ottoman Empire, he was the founder of and contributor to many literary movements and institutions, including his flagship Servet-i Fünun ("The Wealth of Knowledge") journal. He was a strong critic of the Sultan Abdul Hamid II, which led to the censorship of much of his work by the Ottoman government. His many novels, plays, short stories, and essays include his 1899 romance novel Aşk-ı Memnu ("Forbidden Love"), which has been adapted into an internationally successful television series of the same name.'

from tmpcode import bune

output = bune(soru)
open('tmpoutput', 'w').write(output)
if output.strip() != answer:
    print('Beklenen Çıktı bu soru için verilmemektedir')
    exit(1)
exit(0)
