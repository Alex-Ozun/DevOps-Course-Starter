# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

## Set Environment Variables

Flast uses `.env` file to set environment variables when running `flask run`.

1. Run `$ cp .env.template .env  # (first time only)`
1. Add following variables in .env:
- [`SECRET_KEY`](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY): used to encrypt the flask session cookie.
- `TRELLO_KEY` and `TRELLO_TOKEN`: Trello API credentials which can be obtained from the [Trello Developer API keys page](https://trello.com/app-key).
- `BOARD_KEY`: the KEY of the Trello board to use for the tasks.

## Run with Docker

Install the latest version of [Docker](https://docs.docker.com/engine/install/)

**Development Mode**

Run 

```bash 
docker compose up
```

**Production Mode**

Run 

```bash 
make
```

## Run with Vagrant

1. Install [Vagrant](https://www.vagrantup.com/downloads) and [VirtualBox](https://www.virtualbox.org/)
1. Run `vagrant up` in the project directory. The initial set-up process will take a few minutes, and then the application will run on [`http://localhost:5000/`](http://localhost:5000/). The application logs can be found in `.vagrant/log.txt`.

## Run Manually

- Install `poetry`: 

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

- Install Dependencies. The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
poetry install
```

- You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup. The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

```bash
cp .env.template .env  # (first time only)
```

- Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:

```bash
poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

To run the unit and integrations tests, run `poetry run pytest tests`.

To run E2E tests:
1. [Install](https://www.mozilla.org/en-GB/firefox/new/) Firefox Browser.
1. [Download](https://github.com/mozilla/geckodriver/releases) `geckodriver` that is compatible with your OS and CPU.
1. Move `geckodriver` binary to the `bin` directory.
1. Run `poetry run pytest tests_e2e`