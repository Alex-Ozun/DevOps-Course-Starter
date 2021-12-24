import pytest
from os import getenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from helpers import app_with_temp_board

@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless') 
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(executable_path='./bin/chromedriver', options=opts) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    text_box = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element_by_id('field_name'))
    text_box.send_keys('Test Todo')
    submit_button = WebDriverWait(driver, timeout=5).until(lambda d: d.find_element_by_id('submit'))
    submit_button.click()
    time.sleep(5)
    cards = WebDriverWait(driver, timeout=5).until(lambda d: d.find_elements_by_id('card_label'))
    assert cards[len(cards) - 1].text.startswith('Test Todo')