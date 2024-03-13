import requests

url = "https://api.acikkuran.com/surah/{}/verse/{}"

def ayet(sure, ayet):
    response = requests.get(url.format(sure, ayet))
    # print(response.json()['data']['verse'])
    return '{} Suresi {}. Ayet\n\n{}\n\n{}'.format(
        response.json()['data']['surah']['name'],
        ayet,
        response.json()['data']['verse'],
        response.json()['data']['translation']['text']
            )

