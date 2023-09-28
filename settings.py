import requests
from bs4 import BeautifulSoup

def parse_status_page():
    url = "https://status.epicgames.com/"

    response = requests.get(url)

    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все элементы с классом "component-container border-color is-group"
        elements = soup.find_all(class_="component-container border-color is-group")

        # Создаем список для хранения данных
        news_data = []

        # Проходимся по найденным элементам и добавляем их текст в список
        for element in elements:
            news_data.append(element.text)
    else:
        # Обработка ошибки, если запрос не успешен
        news_data = []

    return news_data
