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
babel = Babel(app)


@app.route("/", strict_slashes=False)
def index() -> str:
    """ route for / page """
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
