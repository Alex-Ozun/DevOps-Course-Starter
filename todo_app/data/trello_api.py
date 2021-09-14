import requests

class Card:
    id: str
    list_id: str
    title: str
    checked: bool

    def __init__(self, id: str, list_id: str, title: str, checked: bool):
        self.id = id
        self.list_id = list_id
        self.title = title
        self.checked = checked

class Trello:
    list_id_done: str
    list_id_todo: str
    board_id: str
    key: str
    token: str

    def __init__(self, board_id: str, key: str, token: str):
        self.key = key
        self.token = token
        self.board_id = board_id
        self.list_id_done = None
        self.list_id_todo = None
        self.prepare_board()

    def get_cards(self):
        """
        Fetches all cards from the Trello.

        Returns:
            list: The list of saved items.
        """

        url = f"https://api.trello.com/1/boards/{self.board_id}/cards"

        query = {
        'key': self.key,
        'token': self.token
        }
        cards_json = requests.get(url, params=query).json()
        cards = [Card(card_json['id'], card_json['idList'], card_json['name'], False) for card_json in cards_json]
        return cards

    def get_card(self, id) -> Card:
        """
        Fetches the card with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        cards = self.get_cards()
        return next((card for card in cards if card.id == id), None)

    def prepare_board(self):
        list_names = set([list["name"] for list in self.get_lists_on_board()])
        missing_list_names = [name for name in ['To Do', 'Done'] if not name in list_names]
        for name in missing_list_names:
            self.create_list(name)

    def create_list(self, name):
        """
        Creates list of Trello board
        """
        url = f"https://api.trello.com/1/boards/{self.board_id}/lists"
        query = {
            'key': self.key,
            'token': self.token,
            'name': name,
            'pos': 'bottom'
        }
        r = requests.post(url, params=query)
        return r.json()

    def add_card(self, title):
        """
        Adds a new card with the specified title to the Trello.

        Args:
            title: The title of the item.

        Returns:
            card: The saved card.
        """
        url = "https://api.trello.com/1/cards"

        query = {
        'key': self.key,
        'token': self.token,
        'idList': self.list_id_todo,
        'name' : title
        }
        requests.request("POST", url, params=query)

    def save_card(self, card: Card):
        """
        Updates an existing item in Trello. If no existing item matches the ID of the specified item, nothing is saved.

        Args:
            item: The item to save.
        """
        url = f"https://api.trello.com/1/cards/{card.id}"
        query = {
        'key': self.key,
        'token': self.token,
        'idList': self.list_id_done if card.checked else self.list_id_todo
        }
        requests.put(url, query)

    def get_all_cards(self):
        """
        Fetches all cards on Trello board
        """
        lists = self.get_lists_on_board()

        for list in lists:
            if list['name'] == 'To Do':
                self.list_id_todo = list['id']
            elif list['name'] == 'Done':
                self.list_id_done = list['id']

        cards = self.get_cards()

        for card in cards:
            if card.list_id == self.list_id_done:
                card.checked = True
        return cards

    def get_lists_on_board(self):
        """
        Fetches all lists on Trello board
        """
        url = f"https://api.trello.com/1/boards/{self.board_id}/lists"
        query = {
        'key': self.key,
        'token': self.token
        }
        r = requests.get(url, params=query)
        return r.json()

    def delete_item(self, id):
        """
        Deletes an item from the Trello.

        Args:
            id: The ID of the item to be deleted.
        """
        query = {
        'key': self.key,
        'token': self.token
        }
        url = f"https://api.trello.com/1/cards/{id}"

        response = requests.request("DELETE", url, params=query)
        print(response)
