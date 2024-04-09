#!/usr/bin/env python3
""" Module for python flask app """
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Dict
import pytz
from datetime import datetime


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


@babel.localeselector
def get_locale() -> str:
    """ returns the best match with app supported languages """
    lang = request.args.get("locale", None)
    languages = app.config["LANGUAGES"]
    if lang in languages:
        return lang
    if g.user:
        locale = g.user.get("locale", None)
        if locale is not None and locale in languages:
            return locale
    lang = request.headers.get("locale", None)
    if lang in languages:
        return lang
    return request.accept_languages.best_match(languages)


@babel.timezoneselector
def get_timezone():
    """ returns the best match with app supported languages """
    time_zone = request.args.get("timezone", None)
    if time_zone:
        try:
            zone = pytz.timezone(time_zone).zone
            return zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return app.config["BABEL_DEFAULT_TIMEZONE"]


@app.before_request
def before_request() -> None:
    """ Adds user to a fask global user variable """
    g.user = get_user()
    time_now = datetime.now(tz=pytz.UTC)
    locale = get_timezone()
    user_local_time = time_now.astimezone(pytz.timezone(locale))
    time_format = "%b %d, %Y %I:%M:%S %p"
    g.formatted_time = user_local_time.strftime(time_format)


@app.route("/", strict_slashes=False)
def index() -> str:
    """ route for / page """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
