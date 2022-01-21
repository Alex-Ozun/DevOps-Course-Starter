import dotenv
from os import getenv
from pathlib import Path
import pytest
import unittest.mock

import todo_app.app

@pytest.fixture
def client():
    file_path = Path.cwd().joinpath(".env.test")
    dotenv.load_dotenv(file_path, override=True)
    test_app = todo_app.app.create_app()
    with test_app.test_client() as client:
        yield client

def mock_trello_requests(url, params):
    BOARD_KEY = getenv('BOARD_KEY')
    if url == f'https://api.trello.com/1/boards/{BOARD_KEY}/lists':
        response = unittest.mock.Mock()
        response.json.return_value = [
            {'id': '6143905e665dfd3597927908', 'name': 'To Do'},
            {'id': '6143905e665dfd3597927909', 'name': 'Done'},
        ]
        return response
    elif url == f'https://api.trello.com/1/boards/{BOARD_KEY}/cards':
        response = unittest.mock.Mock()
        response.json.return_value = [
            {
                'id': 'card_1',
                'idList': 'to_do_list',
                'name': 'To Do Card',
            },
            {
                'id': 'card_2',
                'idList': 'done_list',
                'name': 'Done Card',
            },
        ]
        return response
    return None

@unittest.mock.patch('requests.get')
def test_index_page(mock_requests_get, client):
    mock_requests_get.side_effect = mock_trello_requests
    response = client.get('/')
    assert response.status_code == 200
    decoded_response = response.data.decode('utf-8')
    assert 'card_1' in decoded_response
    assert 'card_2' in decoded_response
