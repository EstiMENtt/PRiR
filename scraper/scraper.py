import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import asyncio
import aiohttp
from aiohttp import ClientSession
from multiprocessing import Pool
import os

# MongoDB client setup
mongo_url = os.getenv('MONGO_URL', 'mongodb://mongo:27017')
client = MongoClient(mongo_url)
db = client['scraping_db']
profile_collection = db['profiles']
ad_links_collection = db['ad_links']

# Funkcja do parsowania danych ze stron
async def fetch_and_parse(session, url, category):
    async with session.get(url) as response:
        content = await response.read()
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')

        # Znajdź wszystkie ogłoszenia
        ads = soup.find_all('div', {'class': 'list darm'})
        print(f"Found {len(ads)} ads in {category}")

        tasks = [process_ad(session, ad, category) for ad in ads]
        await asyncio.gather(*tasks)

async def process_ad(session, ad, category):
    link_tag = ad.find('a', href=True)
    if link_tag:
        link = "https://www.portel.pl" + link_tag['href']
        print(f"Processing ad link: {link}")

        if category in ['towarzyskie', 'ksiazki', 'nieruchomosci', 'praca', 'motoryzacyjne', 'uslugi', 'dom_i_ogrod', 'elektronika', 'nauka', 'drobne']:
            await process_general_ad(session, link, category)

async def process_general_ad(session, link, category):
    async with session.get(link) as ad_response:
        ad_content = await ad_response.read()
        ad_soup = BeautifulSoup(ad_content, 'html.parser', from_encoding='utf-8')

        data_section = ad_soup.find('fieldset', {'class': 'nier'})
        if data_section:
            divs = data_section.find_all('div', class_='lewyN2')
            if len(divs) >= 8:
                plec = divs[0].text.strip()
                wiek = divs[1].text.strip()
                wzrost = divs[2].text.strip()
                waga = divs[3].text.strip()
                preferencje_seksualne = divs[4].text.strip()
                wyksztalcenie = divs[5].text.strip()
                stan_cywilny = divs[6].text.strip()
                kolor_wlosow = divs[7].text.strip()

                # Zapisz dane do bazy danych
                data = {
                    'płeć': plec,
                    'wiek': wiek,
                    'wzrost': wzrost,
                    'waga': waga,
                    'preferencje seksualne': preferencje_seksualne,
                    'wykształcenie': wyksztalcenie,
                    'stan cywilny': stan_cywilny,
                    'kolor włosów': kolor_wlosow,
                    'link': link,
                    'category': category
                }
                profile_collection.update_one({'link': link}, {'$set': data}, upsert=True)
                print("Data inserted:", data)
            else:
                print("Data section does not contain enough div elements")
        else:
            print("Data section not found")

def parse_data(url, category):
    loop = asyncio.get_event_loop()
    session = ClientSession(loop=loop)
    loop.run_until_complete(fetch_and_parse(session, url, category))
    loop.run_until_complete(session.close())

# Multiprocessing handler
def scrape_category(args):
    url, category = args
    parse_data(url, category)

# Przykładowe użycie
if __name__ == "__main__":
    urls_categories = [
        ("https://www.portel.pl/ogloszenia/nieruchomosci", 'nieruchomosci'),
        ("https://www.portel.pl/ogloszenia/praca", 'praca'),
        ("https://www.portel.pl/ogloszenia/motoryzacyjne", 'motoryzacyjne'),
        ("https://www.portel.pl/ogloszenia/uslugi", 'uslugi'),
        ("https://www.portel.pl/ogloszenia/dom-i-ogrod", 'dom_i_ogrod'),
        ("https://www.portel.pl/ogloszenia/elektronika", 'elektronika'),
        ("https://www.portel.pl/ogloszenia/nauka", 'nauka'),
        ("https://www.portel.pl/ogloszenia/drobne", 'drobne'),
        ("https://www.portel.pl/ogloszenia/damsko-meskie/towarzyskie/", 'towarzyskie'),
        ("https://www.portel.pl/ogloszenia/drobne/ksiazki-i-podreczniki", 'ksiazki')
    ]

    with Pool(processes=10) as pool:
        pool.map(scrape_category, urls_categories)
