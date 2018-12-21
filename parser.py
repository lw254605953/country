from requests_html import HTMLSession
import copy, json

SESSION = HTMLSession()
R = SESSION.get('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html')
COUNTRY = []
percent = 1
# 1. 获取所有省、直辖市的code和名称
for province_data in R.html.find("tr.provincetr td", first=False):
    province = {"name":province_data.text}
    for p_url in province_data.absolute_links:
        # 2. 获取所有市级、直辖市区的code和名称
        citys = []
        P = SESSION.get(p_url)
        print("正在获取数据%d/%d" % (percent, len(R.html.absolute_links) - 1))
        for index, item in enumerate(P.html.find("tr.citytr td", first=False)):
            city = {["code", "name"][index%2] : item.text}
            for C_url in item.absolute_links:
                regions = []
                C = SESSION.get(C_url)
                # 3. 获取所有县级、县级市、直辖市行政区的code和名称
                for i, obj in enumerate(C.html.find("tr.countytr td", first=False)):
                    region = {["code", "name"][i%2] : obj.text}
                    if len(regions) <= i//2:
                        regions.append(region)
                    else:
                        regions[i//2].update(region)
                city["regions"] = regions            
            if len(citys) <= index//2:
                citys.append(city)
            else:
                citys[index//2].update(city)
    # print(citys)
    province["citys"] = citys
    COUNTRY.append(province)
    percent += 1

FO = open("country.json", "w", encoding="utf-8")
FO.write(json.dumps(COUNTRY))
FO.close()
