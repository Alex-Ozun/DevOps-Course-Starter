from flask import abort, Flask, render_template, request, redirect, session, url_for
from todo_app.data.trello_api import Trello
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
    items = trello.get_all_cards()
        
    if request.method == 'GET':
        items.sort(key=is_checked)
        return render_template('index.html', items=items)
    elif request.method == 'POST':
        if new_item := request.form['field_name']:
            trello.add_card(new_item)

        if deleted_item_ids := [key[7:] for key in request.form.keys() if key.startswith('delete_')]:
            print(deleted_item_ids)
            for id in deleted_item_ids:
                trello.delete_item(id)
            return redirect('/')

        all_ids = [str(item.id) for item in items]
        checked_item_ids = request.form.getlist('item')
        checked_items = [trello.get_card(id) for id in checked_item_ids]
        unchecked_items = [trello.get_card(id) for id in all_ids if id not in checked_item_ids]

        for item in checked_items:
            item.checked = True
            trello.save_card(item)

        for item in unchecked_items:
            item.checked = False
            trello.save_card(item)

        return redirect('/')
    else:
        abort(405)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def is_checked(item) -> bool:
  return item.checked


if __name__ == '__main__':
    app.run()
