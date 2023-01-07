import requests
from bs4 import BeautifulSoup
import fake_useragent
def parse():
    link = 'https://rozetka.com.ua/ua/search/?text=Xbox+360'
    headers = {
        'User-Agent': fake_useragent.UserAgent().random
    }
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_ = 'goods-tile__inner')
    comps = []
    for item in items:
        comps.append({
            'title': item.find('span', class_ = 'goods-tile__title').get_text(strip=True),
            'price': item.find('span', class_ = 'goods-tile__price-value').get_text(strip=True),
            'link': item.find('a', class_ = 'goods-tile__heading ng-star-inserted'). get('href')
        })
        for comp in comps:
            print(f"{comp['title']} по цене -> {comp['price']}, ссылка -> {comp['link']}\n")
    for i in range(1, len(comps)+1):
        pass
    print(i)
parse()