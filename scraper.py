import asyncio
import aiohttp
from multiprocessing import Pool
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.scraping_db

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Ekstrakcja danych na podstawie profilu
    data = {}
    # Przykład ekstrakcji adresów email
    data['emails'] = [a['href'] for a in soup.find_all('a', href=True) if 'mailto:' in a['href']]
    return data

def save_to_db(data):
    db.data.insert_one(data)

async def process_url(url):
    html = await fetch(url)
    data = parse(html)
    save_to_db(data)

def main(urls):
    loop = asyncio.get_event_loop()
    tasks = [process_url(url) for url in urls]
    loop.run_until_complete(asyncio.gather(*tasks))

if __name__ == '__main__':
    urls = ['http://example.com', 'http://example.org']
    with Pool(processes=4) as pool:
        pool.map(main, [urls])
