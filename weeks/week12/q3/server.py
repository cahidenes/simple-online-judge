from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import json

app = FastAPI()

result='/iste_linki_buldun_seni_tebrik_ediyorum_fakat_henuz_soru_bitmedi_daha_fotoyu_indirip_asil_sifreyi_bulman_lazim_bu_yolda_sana_kolay_gelsin'

data = [
("XRI57MhCsFYda1IYzshz", 706, 971),
("NWOw3a9EpvBvzT8pbA4D", 169, 251),
("Jn1NwabuO4sMidb3swdT", 672, 324),
("ZT4sJapZ6sR2MLwU5tJD", 973, 761),
("S6170LmjUYQj3fiFsTgb", 251, 351),
("9AwtxFtOcgYAUPCMUg9G", 384, 325),
("OkVQXVKiRNxoJtXJgsc6", 566, 78),
("mVAKM3c9JQJw5R8ZsNuo", 253, 691),
("huUFJeBoGRok7z53QLzR", 319, 606),
("XmcYSOjLU4RENKvTJ8NB", 104, 800),
("dwiPannGj73cMcfRnEr4", 933, 900),
("QGKS9mQMzJ8eh3XIh109", 861, 534),
("PDmGBJkjwkRARxkhG5nP", 962, 674),
("a5dQNeSIXpWQg5X2Ldw1", 576, 756),
("LVIA8nXEc36o7XNoNRb0", 262, 905),
("n5iKibaruLVSVzwWXMia", 144, 682),
("vpijQcqdJd1P731DCioO", 898, 3),
("DwIoo3yiMwVB7koVJQ6m", 500, 911),
("mwDlPERTfPYDI1xVwBOU", 516, 751),
("UxfA6ewbofkT0JiK4w4O", 666, 471),
("B0ybzVa5kZ0YRUmF7oxW", 840, 658),
("IhqNxXb9qeoeMgYdfun4", 505, 970),
("QRlsG7o5dfoJhzQjPJOY", 791, 56),
("kFPl9c0jLUZFVw5yYJlh", 848, 714),
("QLVLN0nOuyGPtGWXgIZB", 984, 290),
("gKJiYo7dEke5dej7o5wl", 98, 91),
("KN9ECeTJbq3LRrX5jxwF", 784, 288),
("ZECOc3qsjkwf80qsggMl", 933, 649),
("QDcCoJCeKJbeoVGScsnK", 698, 624),
("NtQdRuUtNzZfyn0MVfa3", 757, 906),
("9oLvSX9MxOF3Nkp7eiZL", 554, 656),
("39NNMbMJsQbrcVOhDMON", 937, 475),
("nhGM6cD7vQWyq63EUeTm", 190, 983),
("cs62imUL2lwK4GDzMtVA", 985, 509),
("MjIe0SzcBApWxYDTO966", 187, 425),
("YTEz57jJ3O2OKYrUd3e0", 572, 225),
("9bXOxAuyLDb2xL0DYSal", 804, 944),
("ZAJJ1JvyrUQ8JJhBMKAx", 692, 120),
("zyhMgqTwrw99qWePvXDZ", 828, 673),
("WBiaBy8gFTYkc4pLfEeg", 495, 927),
("LyM87fgjxTGIoUVJiEgO", 69, 561),
("n1R288lldAOhNghweM9c", 862, 228),
("c7R5roS9UaCp7JEpa3tJ", 647, 38),
("xTWOxaRyrV3ZS0fkWMCS", 142, 475),
("2MMnQJxO2BIt1gFLJYzZ", 877, 108),
("elq32EqVKs0cM8JNkbuh", 175, 547),
("vmU8r4n09VUWWhIvNWpN", 509, 54),
("O5G1YCJE0PbzdUZ3V7Mr", 435, 914),
("q4KZsKCizEyAd5Jj0wGO", 492, 955),
("Qo9XYL3ozzvVULf1uTCF", 210, 327),
("pig6iYCrs5TX6xEg0GU7", 840, 292),
("W0SGwxmDBdvf8O5aa8IC", 321, 96),
("Ofp1acICvsbfNfMMvW3d", 120, 964),
("01RxT5rGu1Fb0fNbmEYr", 722, 884),
("CeCtpA4b1XuU3JBF7qyG", 497, 175),
("Bp1Q1mmT7BofN84vru96", 531, 316),
("26B4acfxMAgCWai3wYOK", 573, 613),
("xpBGli1qCOPiK4kp2qnx", 376, 5),
("YOZITPB2yLfR2fkwnqKN", 948, 529),
("lubVbVPWSsJgny2CdlfW", 938, 264),
("deXekhjCUdPAsmnfPgCO", 40, 422),
("LO0z9AJiY3xc1RJn11kf", 848, 477),
("KcqcLQl3BToJQvv0el0W", 582, 176),
("TnFNU3YfIy4QsdBzaJsg", 731, 863),
("dZw0APFvJb3DJW8hjrxO", 593, 300),
("W3dYkvZ0itbFTSJPW504", 733, 314),
("mpcchI9tWR1UiiLt1xLA", 249, 70),
("SojTsARZNbJPN3DOaSPD", 974, 509),
("n8KbhA8K9iqSUvRXhk4r", 654, 754),
("1VNwLYEWmRbuqAmJjdqF", 278, 504),
("kp56FDfXSClsd7WQ5Qzs", 965, 934),
("pPln5IvdrN2Jm9QeL7JE", 377, 686),
("FWGJIskndJvh4DgLvGNR", 477, 94),
("lYucMRlrsJTVV0yMoswO", 237, 720),
("4Ak3XgjFOY4XuGxgiqpr", 306, 358),
("hb2shkJINb0F0Vxa8h8p", 210, 91),
("WPSdyR5fcejcJA4VR6go", 458, 551),
("6ytDusGc3R2TwQVYSiWy", 319, 657),
("RSCjxprD9yFJL08j3yeL", 743, 380),
("5ngMGI5N9z65jzkGciJM", 213, 465),
("Cxq89YGJxW1rZvVRE9c6", 141, 63),
("AWBE3zi7Cdu7NIbAfoqB", 156, 387),
("q39cJaRqGA7BTohR9z5R", 469, 859),
("Q3JPUSXjJy7y2G9wr63p", 274, 63),
("2nxID0mgmTY2eeS78rGE", 715, 703),
("ZpqkqoEp3MD2FSYBn2Ma", 801, 629),
("kScPajBXyqtqmCALqNQM", 805, 849),
("gEgc2ZNoFEQJv0qnKCnW", 398, 562),
("QKLUUM21Xy11upmtzSpq", 82, 475),
("RGuOOsC4A0p6ATXR7u0r", 472, 266),
("NxYS77VvbGB0tuUuioj9", 104, 697),
("hay03IxakdeAeis14nLX", 894, 914),
("BW2orXqQSpJACBqgJ93f", 632, 83),
("ecgn3u58cjLIbrkpPSk2", 684, 330),
("uG4LBhMMoWh7sGvElRTa", 716, 155),
("bn5ImkEGmr4VvLxeB4bT", 808, 663),
("Gxr3b1oZIvp3nyIXP9ag", 275, 161),
("QMjDzPh6ITO0xbCJosSS", 737, 897),
("IuKJ7CMEzMd32jkrS9wy", 728, 497),
("4fmxXCWn03jobkdkMNM5", 592, 102),
("bp4Ogt5ekoQsfM98mUjA", 45, 530),
("LOD2yuK3aoXcKzuWUCf0", 51, 762),
("6WyjK5nE5gnMlLY5EAG1", 706, 672),
("rEorL7SMD00jI0Z6KByl", 24, 189),
("MeZw0a19naE3CVgJwz64", 123, 382),
("EugeIg6r83QyRRL3biZ3", 372, 595),
("7N7lw9iPMOGdXFBVeZ6g", 40, 291),
("YxF6RnA6ATOK4eJzSJcn", 528, 858),
("9n7DoGIp4LjJOK6nlQxk", 211, 858),
("J1pugFGG8AoerbOJOO8c", 567, 336),
("g0LKTOtKOptF6EceXErY", 453, 124),
("qmT9IcalLGc3Ja9J7KQW", 462, 646),
("BtKWMjEkV45B8cuDI8ua", 491, 110),
("2WERc80m2RJdljAoBcsN", 252, 614),
("kedJDDr6sW1aAUzPBO45", 982, 276),
("SzKIXlW5vjY9fJr95IMr", 379, 705),
("RE1Yw35g0oQVa9N0lvj8", 717, 721),
("xoX5hwjNAwekAxoa52np", 832, 54),
("mPckOXSjDagRneSRT5ZU", 684, 449),
("bCKKIaYCN17asF0lRXnE", 370, 628),
("USkdmpJOrLkpwkJDE8Q7", 642, 519),
("C7Et8ch1jUyyANp8AFq6", 112, 352),
("qwovX2taIgQvBVOIpA8k", 669, 420),
("EP9TlaPj77RUTkJzrsfq", 885, 288),
("fEQ3i1yTyXC7NfXcQRsO", 395, 810),
("1dFYkMo1QN2kXYVB4mWr", 176, 624),
("lVjD93JT4FlWPaZ75b2h", 67, 826),
("rjGQcVcwJGQ7RnP8NrhK", 978, 306),
("0G7pwLmlVRGxnWf41DJN", 29, 501),
("6EZq59V479BcwV8ZxZjs", 767, 510),
("ArUZpjNXgKW6SZlJrT91", 697, 686),
("knvp4SCJFdjqJDIphCpM", 451, 673),
("mTE0tS9sXa6cTm2qeTdg", 377, 960),
("4U5M07LiYmoJut7rV1U2", 54, 324),
("TGyJT3aDA34UwRZtD7eF", 811, 399),
("KdGdhhYS1TzuPcpnJ3fN", 890, 768),
("ZuU7OowtAmiVI1O3bqKX", 357, 7)
]


@app.get("/")
def read_root(harf: int):
    dic = {"bulbakalimlinki": {
        "budegil": "budegil",
        "bune": 
            [{"dogrugidiyorsun": {
                "challange": {
                    "a": data[harf][1],
                    "b": data[harf][2],
                },
                "birsonrakindeidvar": "burdayok",
                "buradangit": [data[harf][0]],
                "bironcekindeydikacirdin": "hehee"
                }}],
        "budadegil": "budadegil"
        }}
    return JSONResponse(content=dic)

@app.get("/cevapla")
def cevapla(id: str, cevap: int):
    for num, (_id, a, b) in enumerate(data):
        if id == _id:
            if a + b == cevap:
                return {"harf": result[num]}
            else:
                return {"harf": "Cevap Yanlış"}



@app.get("/iste_linki_buldun_seni_tebrik_ediyorum_fakat_henuz_soru_bitmedi_daha_fotoyu_indirip_asil_sifreyi_bulman_lazim_bu_yolda_sana_kolay_gelsin")
def read_item():
    return HTMLResponse(content="<img src='https://i.ibb.co/PCxSQDQ/sifre.png' />")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


