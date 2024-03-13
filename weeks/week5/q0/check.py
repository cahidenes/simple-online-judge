try:
    from tmpcode import ayet
    import requests

    url = "https://api.acikkuran.com/surah/{}/verse/{}"

    def myayet(sure, ayet):
        response = requests.get(url.format(sure, ayet))
        # print(response.json()['data']['verse'])
        return '{} Suresi {}. Ayet\n\n{}\n\n{}'.format(
            response.json()['data']['surah']['name'],
            ayet,
            response.json()['data']['verse'],
            response.json()['data']['translation']['text']
        )

    if ayet(10, 7) != myayet(10, 7):
        print("Olmadı")
        exit(1)
    if ayet(2, 185) != myayet(2, 185):
        print("Olmadı")
        exit(1)
    if ayet(80, 3) != myayet(80, 3):
        print("Olmadı")
        exit(1)
    if ayet(112, 1) != myayet(112, 1):
        print("Olmadı")
        exit(1)
    if ayet(38, 38) != myayet(38, 38):
        print("Olmadı")
        exit(1)

    exit(0)
except Exception as e:
    print(e)
    exit(1)
