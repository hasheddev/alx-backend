#!/usr/bin/env python3
""" Module for python flask app """
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Dict


class Config:
    """ contains flask app configurations """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Dict:
    """ searches for user in dictionary and returns user or None if not
    found"""
    user_id = request.args.get("login_as", None)
    if user_id is not None and int(user_id) in users:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """ Adds user to a fask global user variable """
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """ returns the best match with app supported languages """
    lang = request.args.get("locale", None)
    languages = app.config["LANGUAGES"]
    if lang in languages:
        return lang
    return request.accept_languages.best_match(languages)


@app.route("/", strict_slashes=False)
def index() -> str:
    """ route for / page """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
