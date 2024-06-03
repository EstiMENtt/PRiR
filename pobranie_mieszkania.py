import requests
from bs4 import BeautifulSoup

# Adres URL do skrapowania
url = 'https://www.portel.pl/ogloszenia/nieruchomosci/lokale-mieszkalne/chcesz-sprzedac-wynajac-swoje-mieszkanie-nie/785584?nd=1'

# Wyślij żądanie do strony i pobierz jej zawartość
response = requests.get(url)

# Sprawdź, czy żądanie było udane
if response.status_code == 200:
    # Przetwórz zawartość strony za pomocą BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Zapisz link do danych
    link_do_danych = url

    # Znajdź elementy zawierające dane nieruchomości
    dane_nieruchomosci = soup.find('fieldset', class_='nier')

    # Pobierz poszczególne informacje o nieruchomości, jeśli istnieją
    powierzchnia = dane_nieruchomosci.find('div', class_='lewyN2').text.strip() if dane_nieruchomosci else None
    pietro = dane_nieruchomosci.find_all('div', class_='lewyN2')[1].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 1) else None
    cena = dane_nieruchomosci.find_all('div', class_='lewyN2')[2].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 2) else None
    liczba_pokoi = dane_nieruchomosci.find_all('div', class_='lewyN2')[3].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 3) else None
    lokalizacja = dane_nieruchomosci.find_all('div', class_='lewyN2')[4].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 4) else None
    typ_zabudowy = dane_nieruchomosci.find_all('div', class_='lewyN2')[5].text.strip() if (dane_nieruchomosci and len(dane_nieruchomosci.find_all('div', class_='lewyN2')) > 5) else None

    # Znajdź elementy zawierające dane kontaktowe
    dane_kontaktowe = soup.find('fieldset', class_='kontakt')

    # Pobierz adres i numery telefonów, jeśli istnieją
    adres = dane_kontaktowe.find('div', class_='lewagr').find('h5').text.strip() if dane_kontaktowe else None
    tel = dane_kontaktowe.find('div', id='telkon').find('h5').text.strip() if dane_kontaktowe.find('div', id='telkon') else None
    kom = dane_kontaktowe.find('div', id='gsmkon').find('h5').text.strip() if dane_kontaktowe.find('div', id='gsmkon') else None

    # Wyświetl pobrane dane
    print("Link do danych:", link_do_danych)
    print("\nDane nieruchomości:")
    print("Powierzchnia:", powierzchnia)
    print("Piętro:", pietro)
    print("Cena:", cena)
    print("Liczba pokoi:", liczba_pokoi)
    print("Lokalizacja:", lokalizacja)
    print("Typ zabudowy:", typ_zabudowy)

    print("\nDane kontaktowe:")
    print("Adres:", adres)
    print("Tel.:", tel)
    print("Kom.:", kom)

else:
    print("Nie można pobrać zawartości strony.")
