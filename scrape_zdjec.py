import requests
from bs4 import BeautifulSoup
import os

# URL strony do scrapowania
url = 'https://www.portel.pl/ogloszenia/nieruchomosci/domy-mieszkalne/dom-drewniany-jednorodzinny-mini-i-jestesmy/786672?nd=1'

# Pobieranie zawartości strony
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Znajdź wszystkie elementy <img> wewnątrz <div class='fotocont0'>
image_divs = soup.find_all('div', class_='fotocont0')

# Katalog docelowy, gdzie zostaną zapisane obrazy
download_dir = 'scraped_images'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Iteracja przez znalezione divy
for div in image_divs:
    # Znajdź wszystkie linki do obrazów
    image_links = div.find_all('a', class_='swipebox')
    for link in image_links:
        # Pobierz adres URL obrazu
        img_url = 'https://www.portel.pl' + link['href']
        # Uzyskaj nazwę pliku obrazu z adresu URL
        img_name = img_url.split('/')[-1]
        # Utwórz pełną ścieżkę do pliku docelowego
        img_path = os.path.join(download_dir, img_name)
        # Pobierz obraz
        img_data = requests.get(img_url).content
        # Zapisz obraz na dysku
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
            print(f"Zapisano: {img_name}")
