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

FROM base as test
RUN apt-get update && apt-get install -y chromium-driver && rm -rf /var/lib/apt/lists/*
RUN mkdir bin && ln -s /usr/bin/chromedriver bin/chromedriver
# ENV LANG=en_GB.UTF-8
ENTRYPOINT ["poetry", "run", "pytest"]
