import pytest
import dotenv
from os import getenv
import requests
from todo_app import app
from threading import Thread

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
