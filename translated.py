import pprint

import requests



def get_translator(sl:str, dl:str, text:str):
    sl = sl
    dl = dl
    text = text
    lagn = requests.get('https://ftapi.pythonanywhere.com/languages')
    res = requests.get(f'https://ftapi.pythonanywhere.com/translate?sl={sl}&dl={dl}&text={text}')
    data = res.json()
    data_lang = lagn.json()
    result = '\n'.join(data['translations']['possible-translations'])
    return result


