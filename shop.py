import requests
from bs4 import BeautifulSoup

def scrape_image_urls():
    # Ваш URL страницы
    site_url = 'https://universofortnite.com/ru/tienda-de-hoy-en-fortnite/'

    # URL-адреса изображений, которые нужно исключить
    excluded_image_urls = [
        'https://universofortnite.com/wp-content/plugins/gtranslate/flags/24/es.png',
        'https://universofortnite.com/wp-content/uploads/2021/03/Logo-Footer-Universo-Fortnite-300x71.png',
        'https://universofortnite.com/wp-content/uploads/2021/03/pavos-gratis-para-fortnite-168x88.jpg',
        'https://universofortnite.com/wp-content/uploads/2021/03/conseguir-skins-gratis-en-fortnite-168x88.jpg',
        'https://universofortnite.com/wp-content/uploads/2021/03/tienda-de-hoy-fortnite-actualizada-1-168x88.jpg',
        'https://universofortnite.com/wp-content/uploads/2021/03/consejos-para-ganar-en-fortnite-168x88.jpg',
        'https://universofortnite.com/wp-content/plugins/social-media-widget/images/cutout/64/youtube.png',
        'https://universofortnite.com/wp-content/plugins/social-media-widget/images/cutout/64/twitter.png',
        'https://universofortnite.com/wp-content/plugins/social-media-widget/images/cutout/64/facebook.png',
        'https://universofortnite.com/wp-content/uploads/2021/03/Logo-Universo-Fortnite-1.png'
    ]

    try:
        # Запрашиваем страницу
        response = requests.get(site_url)
        response.raise_for_status()

        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все изображения на странице и сохраняем их URL-адреса в список
        image_urls = []
        images = soup.find_all('img')
        for img in images:
            img_url = img.get('src')  # Получаем URL изображения
            if img_url and img_url not in excluded_image_urls:
                image_urls.append(img_url)

        return image_urls

    except Exception as e:
        # Если произошла ошибка, выводим сообщение об ошибке
        print(f"Произошла ошибка: {str(e)}")
        return []

