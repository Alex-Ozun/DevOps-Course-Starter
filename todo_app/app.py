from flask import abort, Flask, render_template, request, redirect, url_for

from todo_app.data.session_items import get_items, add_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        items = get_items()
        return render_template('index.html', items=items)
    elif request.method == 'POST':
        add_item(request.form['new_item'])
        return redirect(url_for('index'))
    else:
        abort(405)

if __name__ == '__main__':
    app.run()
