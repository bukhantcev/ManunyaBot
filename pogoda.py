import pprint

import requests

appid = "de0fdaaacab98bc09e3e5e3504358c50"


def get_pogoda(s_city: str):
    s_city = s_city
    city_id = 0
    result = ''
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
        pass

    # try:
    #     res = requests.get("http://api.openweathermap.org/data/2.5/weather",
    #                  params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    #     data = res.json()
    #     print("conditions:", data['weather'][0]['description'])
    #     print("temp:", data['main']['temp'])
    #     print("temp_min:", data['main']['temp_min'])
    #     print("temp_max:", data['main']['temp_max'])
    # except Exception as e:
    #     print("Exception (weather):", e)
    #     pass
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            if i['dt_txt'].split(' ')[1].split(':')[0] == '12':
                result_1 = i['dt_txt'].split(" ")[0], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description']
                result = result + '\n' + f"{' '.join(result_1)}"
        pprint.pprint(str(data['list'][0]['dt_txt']).split(' ')[1].split(':')[0])
        return result
    except Exception as e:
        print("Exception (forecast):", e)
        pass



