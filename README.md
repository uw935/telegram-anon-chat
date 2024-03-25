<br>
<p align="center">
    <img align="center" src="media/thumbnail.png">
    <h3 align="center">Telegram anonymous chat</h3>
    <p align="center">Chat-bot for communicate with random people in Telegram</p>
</p>
<br>

## About
This bot made for communication between random people in chat with saving anonymousity.

Project is written like pet in Python 3.8.10 using aiogram.


### How is it working
1. Users press the button or type "/newchat" command
2. Fetching pseudorandom people from the **users in searching** list
3. If there is no people from the list, sending user to wait while he will be selected by another user randomly.
4. If user found, just start chatting

### Commands
General commands

- **/newchat** — start new chat
- **/stopchat** — stop this chat

### How to start
```shell
docker-compose up --build
```

### References
Outside resources that was taken for the bot

- [Interesting facts API](https://uselessfacts.jsph.pl/)

## Contributing

All the files here are under the MIT License. I'd really appreciate if you add something new to this project or make some feature plans from TODO below.

If you have any troubles with contributing, just write me in Telergam (contacts in the section below), I can help you.

### Environment variables
Change .env file to your settings.

```.env
BOT_TOKEN = "BOT_TOKEN_FROM_BOTFATHER"
DB_URL = "sqlite://path/to/db"
```

### Setting up an environment

```shell
cd src
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
```

### Creating the database
```shell
python

>>> from db import engine
>>> from db.models.users import Base 
>>> Base.metadata.create_all(bind=engine)
```

### Starting application

```shell
python main.py
```

### Rules
1. **Important**: Before create PR, you should check code with the **flake8** module.

### TODO
- [ ] move from the .sqlite DB to the mysql or postgresql
- [ ] make bot alive (find server to deploy it)
- [x] interesting facts while waiting new chat
- [ ] admin panel

## Author
Made by [@uw935 — contacts](https://uw935.com/) with love.
