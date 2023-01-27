import datetime

print(datetime.date.fromtimestamp(400000000))

####

#import requests
# from bs4 import BeautifulSoup
# url='http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
# r=requests.get(url)
# r.encoding=r.apparent_encoding
# soup=BeautifulSoup(r.text,'html.parser')
# items=soup.find('ul',class_='nav nav-list').find('li').find_all('li')
# for item in items:
#     print(item.text.strip())#strip()可以清除文本首位的空格


