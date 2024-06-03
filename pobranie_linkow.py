import requests
from bs4 import BeautifulSoup

# Pobieranie linków dla zakresu od 0 do 2
links = []
for i in range(2):
    url = f"https://www.portel.pl/ogloszenia/nieruchomosci?ns={i}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all("div", class_="list plat")
    links += [element.find("a")["href"] for element in elements]

# Wyświetlenie znalezionych linków
for link in links:
    print(link)
