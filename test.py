import requests
from bs4 import BeautifulSoup as BS

def parse_news():
    news_url = 'https://portalvirtualreality.ru/tag/novosti-fortnajt/'
    response = requests.get(news_url)

    if response.status_code == 200:
        news_soup = BS(response.content, 'html.parser')
        news_titles = news_soup.find_all("h2", class_="post-title")
        news_excerpts = news_soup.find_all("p", class_="post-excerpt")
        news_images = news_soup.find_all("img")  # Находим все элементы <img>

        news_data = []
        for i in range(min(len(news_titles), len(news_excerpts))):
            title = news_titles[i].text
            excerpt = news_excerpts[i].text
            if i < len(news_images):
                image_url = news_images[i]['src']  # Получаем URL изображения
            else:
                image_url = None
            news_data.append({'title': title, 'excerpt': excerpt, 'image_url': image_url})

        return news_data
    else:
        return []

if __name__ == '__main__':
    news = parse_news()
    for article in news:
        print("Title:", article['title'])
        print("Excerpt:", article['excerpt'])
        print("Image URL:", article['image_url'])
        print()
