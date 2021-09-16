from dataclasses import dataclass
from todo_app.data.trello_api import Card

@dataclass
class ViewModel:
    all_cards: [Card]

    def todo_cards(self):
        return [card for card in self.all_cards if not card.checked]

    def done_cards(self):
        return [card for card in self.all_cards if card.checked]