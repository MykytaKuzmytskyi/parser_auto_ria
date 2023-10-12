import re

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def open_browser():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def close_browser(driver):
    driver.close()


def find_element_with_default(driver, by, value, default=None):
    try:
        element = driver.find_element(by, value)
        return element.text
    except NoSuchElementException:
        return default


def get_car_number(driver):
    return find_element_with_default(driver, By.CLASS_NAME, "state-num.ua")


def get_car_vin(driver):
    value = find_element_with_default(driver, By.CLASS_NAME, "label-vin")
    if value is None:
        value = find_element_with_default(driver, By.CLASS_NAME, "vin-code")
    return value


def get_data(url: str, driver):
    driver.get(url)

    title = find_element_with_default(driver, By.CSS_SELECTOR, ".heading .head")
    price_usd = int(re.sub(r'[^0-9]', '', find_element_with_default(driver, By.CSS_SELECTOR, "strong")))
    odometer = int(find_element_with_default(driver, By.CSS_SELECTOR, "section .base-information.bold .size18")) * 1000
    username = find_element_with_default(driver, By.CSS_SELECTOR, ".seller_info_name")
    image_url = driver.find_element(By.CSS_SELECTOR, ".outline.m-auto").get_attribute("src")
    images_count = int(
        re.sub(r'[^0-9]', '', find_element_with_default(driver, By.CSS_SELECTOR, "span.count > span.mhide")))
    car_number = get_car_number(driver)
    car_vin = get_car_vin(driver)
    button = driver.find_element(By.CLASS_NAME, "size14.phone_show_link.link-dotted.mhide")
    driver.execute_script("arguments[0].scrollIntoView();", button)
    if not button.get_attribute("disabled"):
        button.click()
    phone = re.sub(r'[^0-9]', '', find_element_with_default(driver, By.CSS_SELECTOR, "div.phones_item > span"))
    international_number = '+38' + phone

    value = {
        "url": url,
        "title": title,
        "price_usd": price_usd,
        "odometer": odometer,
        "username": username,
        "phone_number": international_number,
        "image_url": image_url,
        "images_count": images_count,
        "car_number": car_number,
        "car_vin": car_vin,
    }
    return value
