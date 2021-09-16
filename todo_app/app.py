from flask import abort, Flask, render_template, request, redirect, session, url_for
from todo_app.data.trello_api import Trello
from todo_app.data.view_model import ViewModel
from todo_app.flask_config import Config
from os import environ

BOARD_KEY = environ.get('BOARD_KEY')
TRELLO_KEY = environ.get('TRELLO_KEY')
TRELLO_TOKEN = environ.get('TRELLO_TOKEN')

app = Flask(__name__)
app.config.from_object(Config)
trello = Trello(BOARD_KEY, TRELLO_KEY, TRELLO_TOKEN)

@app.route('/', methods=['POST', 'GET'])
def index():
    view_model = ViewModel(all_cards=trello.get_all_cards())
    if request.method == 'GET':
        return render_template('index.html', view_model=view_model)
    elif request.method == 'POST':
        if new_card := request.form['field_name']:
            trello.add_card(new_card)

        if deleted_card_ids := [key[7:] for key in request.form.keys() if key.startswith('delete_')]:
            print(deleted_card_ids)
            for id in deleted_card_ids:
                trello.delete_card(id)
            return redirect('/')

        all_ids = [str(card.id) for card in view_model.all_cards]
        checked_card_ids = request.form.getlist('card')
        checked_cards = [trello.get_card(id) for id in checked_card_ids]
        unchecked_cards = [trello.get_card(id) for id in all_ids if id not in checked_card_ids]

        for card in checked_cards:
            card.checked = True
            trello.save_card(card)

        for card in unchecked_cards:
            card.checked = False
            trello.save_card(card)

        return redirect('/')
    else:
        abort(405)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def is_checked(card) -> bool:
  return card.checked


if __name__ == '__main__':
    app.run()
