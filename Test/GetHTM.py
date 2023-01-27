import re
import requests
from bs4 import BeautifulSoup

url = 'https://www.info.gov.hk/gia/wr/202201/01.htm'

r = requests.get(url, stream=True)
# print(r.text)
soup = BeautifulSoup(r.text, "lxml")
a_tags = soup.find_all('li', string=re.compile("PRESS WEATHER NO. 152"))  # HOURLY READINGS 改變此字眼將增加取用範圍

for tag in a_tags:
    filename = tag.a.string + '.htm'
    domain_url = 'https://www.info.gov.hk/'
    link = tag.a.get('href')
    # print(domain_url + link)

    press = requests.get(domain_url + link, stream=True)
    # print(press.text)
    excel = BeautifulSoup(press.text, "lxml")
    excel_overall = excel.find(id='weather_report')
    word = excel_overall.text
    hkobservatory_temperature = word[word.find("CELSIUS")-11:word.find("CELSIUS")-9]
    hkobservatory_humidity = word[word.find("HUMIDITY")+9:word.find("HUMIDITY")+11]
    place_list = {
        "KING'S PARK",
        "WONG CHUK HANG",
        "TA KWU LING",
        "LAU FAU SHAN",
        "TAI PO",
        "SHA TIN",
        "TUEN MUN",
        "TSEUNG KWAN O",
        "SAI KUNG",
        "CHEUNG CHAU",
        "CHEK LAP KOK",
        "TSING YI",
        "SHEK KONG",
        "TSUEN WAN HO KOON",
        "TSUEN WAN SHING MUN VALLEY",
        "HONG KONG PARK",
        "SHAU KEI WAN",
        "KOWLOON CITY",
        "HAPPY VALLEY",
        "WONG TAI SIN",
        "STANLEY",
        "KWUN TONG",
        "SHAM SHUI PO",
        "KAI TAK RUNWAY PARK",
        "YUEN LONG PARK",
        "TAI MEI TUK",
    }
    for place in place_list:
        position = word.find(place)

        print(place, '的位置是', position, '溫度是')

    # kings_park_word_position = word.find("KING'S PARK")
    # kings_park_temperature = word[word.find("DEGREES", kings_park_word_position)-3:word.find("DEGREES", kings_park_word_position)-1]

    # print(word.find("KING'S PARK"))
    # print(kings_park_word_position)
    # print(kings_park_temperature)

    # print(excel.prettify())

    # with open(filename, 'wb') as fd:
    #     for chunk in press.iter_content(chunk_size=128):
    #         fd.write(chunk)


'''
# filename = r.url.split('/')[-1:]
# print(soup.prettify())
'''
