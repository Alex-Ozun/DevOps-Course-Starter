FROM python:3.9-slim-buster as base

EXPOSE 5050
WORKDIR /todo-app
COPY . /todo-app
RUN pip install "poetry==1.1.10" \
&& poetry config virtualenvs.create false --local \
&& poetry install 

FROM base as development
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5050

FROM base as production
RUN poetry add gunicorn
ENTRYPOINT poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:5050