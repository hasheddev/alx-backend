#!/usr/bin/env python3
""" Module for python flask app """
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """ contains flask app configurations """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel()


def get_locale() -> str:
    """ returns the best match with app supported languages """
    languages = app.config["LANGUAGES"]
    return request.accept_languages.best_match(languages)


babel.init_app(app, locale_selector=get_locale)


@app.route("/", strict_slashes=False)
def index() -> str:
    """ route for / page """
    return render_template('2-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
