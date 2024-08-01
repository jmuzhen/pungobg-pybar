# A simple Flask server to keep the bot alive
# useful on hosting platforms like Repl.it

from threading import Thread

from flask import Flask

app = Flask('')


@app.route('/')
def main():
    return "Telegram bot is running..."


def run():
    app.run(host="0.0.0.0", port=6330)


def keep_alive():
    server = Thread(target=run)
    server.start()
