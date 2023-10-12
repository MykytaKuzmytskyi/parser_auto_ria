import asyncio
from urllib.parse import urljoin

import aiohttp
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup

from auto_card.pars_manager.selenium_parser import get_data, open_browser, close_browser
from auto_card.models import Card

BASE_URL = "https://auto.ria.com/uk/car/used/"


async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()


@sync_to_async
def parse_single_page_sync(data: dict):
    card, created = Card.objects.update_or_create(
        url=data["url"],
        defaults={
            "title": data["title"],
            "price_usd": data["price_usd"],
            "odometer": data["odometer"],
            "username": data["username"],
            "phone_number": data["phone_number"],
            "image_url": data["image_url"],
            "images_count": data["images_count"],
            "car_number": data["car_number"],
            "car_vin": data["car_vin"],
        }
    )


async def process_page(session, url, driver):
    page_content = await fetch_url(session, url)
    soup = BeautifulSoup(page_content, "html.parser")
    if soup.select_one(".notice_head") is None and soup.select_one("section.verifiability") is not None:
        data = get_data(url, driver)
        await parse_single_page_sync(data=data)


async def cards_list():
    num_page = 1
    driver = open_browser()
    while num_page != 101:
        url_num_page = urljoin(BASE_URL, f"?page={num_page}")
        print(f"Parsing page #{num_page} - {url_num_page}")
        async with aiohttp.ClientSession() as session:
            page_content = await fetch_url(session, url_num_page)
            soup = BeautifulSoup(page_content, "html.parser")
            cars = soup.select(".content-bar")
            urls = [urljoin(url_num_page, car.find()["href"]) for car in cars]
            tasks = []
            for url in urls:
                print(url)
                tasks.append(process_page(session, url, driver))

            await asyncio.gather(*tasks)

        num_page += 1

    close_browser(driver)
