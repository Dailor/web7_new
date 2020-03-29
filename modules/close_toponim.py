import requests
import CONST


def find_close(toponim, pos, count_result):
    params = {"ll": ','.join(str(x) for x in pos),
              "apikey": CONST.SEARCH_MAP_KEY,
              "text": toponim,
              "spn": "0.01,0.01",
              "lang": "en_RU"}
    r = requests.get(CONST.API_SEARCH_MAP, params).json()['features']
    obj = list()
    for i in range(count_result):
        temp = dict()
        try:
            features = r[i]
        except Exception:
            break
        temp["pos"] = features["geometry"]["coordinates"]
        temp["box"] = features["properties"]["boundedBy"]
        temp["name"] = features["properties"]["CompanyMetaData"]["name"]
        temp["addr"] = features["properties"]["CompanyMetaData"]["address"]
        try:
            time_info = features["properties"]["CompanyMetaData"]["Hours"]
            temp["time"] = time_info["text"], CONST.COLORS_TIME[time_info["Availabilities"][0]["TwentyFourHours"]]
        except Exception as e:
            key_error = e.args[0]
            if key_error == 'Hours':
                temp['time'] = None, CONST.COLORS_TIME[None]
            elif key_error == 'TwentyFourHours':
                temp['time'] = None, CONST.COLORS_TIME[False]
        obj.append(temp)
    return obj
