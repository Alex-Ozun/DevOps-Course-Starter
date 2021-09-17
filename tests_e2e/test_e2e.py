import pytest
import dotenv
import requests
from os import getenv
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from todo_app import app                  
from threading import Thread
from selenium.webdriver.support.ui import WebDriverWait
import time

@pytest.fixture(scope='module')
def app_with_temp_board(): 
    dotenv.load_dotenv(dotenv.find_dotenv('.env'), override=True)
    key = getenv('TRELLO_KEY')
    token = getenv('TRELLO_TOKEN')
    board_id = create_trello_board(key, token)
    application = app.create_app()
    thread = Thread(target=lambda: application.run(use_reloader=False))    
    thread.daemon = True    
    thread.start()    
    yield application
    thread.join(1)
    delete_trello_board(key, token, board_id)

def create_trello_board(key, token):
    params = { 'key': key, 'token': token, 'name': 'e2e test board', 'defaultLists': 'false' }
    response = requests.post(url='https://api.trello.com/1/boards', params=params)
    return response.json()['id']

def delete_trello_board(key, token, board_id):
    params = { 'key': key, 'token': token }
    response = requests.delete(url=f'https://api.trello.com/1/boards/{board_id}', params=params)
    if response.status_code != 200:
        raise Exception(f'Attempting to delete e2e test board returned status code: {response.status_code}')

@pytest.fixture(scope='module')
def driver():
    with webdriver.Firefox(executable_path='./bin/geckodriver') as driver:
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