from bs4 import BeautifulSoup
import requests

# URL strony do scrapowania
url = 'https://www.portel.pl/ogloszenia/nieruchomosci/domy-mieszkalne/dom-drewniany-jednorodzinny-mini-i-jestesmy/786672?nd=1'

# Pobieranie zawartości strony
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Znajdź element <div> o danym id
target_div = soup.find('div', id='o786672')

# Jeśli znaleziono element, wydrukuj interesującą linię
if target_div:
    # Znajdź interesującą linię wewnątrz elementu div
    target_line = target_div.find('small')
    if target_line:
        # Pobierz tekst z linii i usuń białe znaki z początku i końca
        line_text = target_line.get_text().strip()
        
        # Wyodrębnij numer ogłoszenia i datę
        start_idx = line_text.find('Ogł. nr') + len('Ogł. nr')
        end_idx = line_text.find('z')
        ogloszenie_nr = line_text[start_idx:end_idx].strip()
        data_idx = line_text.find('z') + len('z')
        data = line_text[data_idx:].strip()
        
        # Nazwa pliku do zapisania
        filename = 'ogloszenie.txt'
        
        # Zapisz numer ogłoszenia i datę do pliku .txt
        with open(filename, 'w') as file:
            file.write(f"Numer ogłoszenia: {ogloszenie_nr}\nData: {data}")
        
        print(f"Zapisano numer ogłoszenia ({ogloszenie_nr}) i datę ({data}) do pliku: {filename}")
    else:
        print("Nie znaleziono żądanej linii w elemencie div.")
else:
    print("Nie znaleziono żądanego elementu na stronie.")
