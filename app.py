import random
from collections.abc import Iterator

from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)


def get_items_as_iterator(amount: int = 20) -> Iterator[int]:
    return (random.randint(0, 100) for _ in range(amount))


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World! 13"


@app.route("/example")
def example():  # put application's code here
    # [parse_input]-[BEGIN]
    # Nothing for now
    # [parse_input]-[END]

    # [run_main_handler]-[BEGIN]
    items = get_items_as_iterator(amount=15)
    # [run_main_handler]-[END]

    # [format_output]-[BEGIN]
    list_items_formatted = "".join(f"<li>{item}</li>" for item in items)
    # return f'<ul>{list_items_formatted}</ul>'
    return f"<ol>{list_items_formatted}</ol>"
    # [format_output]-[BEGIN]

    # return ''.join(f'<p>{random.randint(0, 100)}</p>' for _ in range(20))


@app.route("/greetings/<name>/<int:age>")
def greetings_by_path(name: str, age: int):  # put application's code here
    return f"Hi, {name}. You are {age} old."


@app.route("/greetings-2")
@use_args({"name": fields.Str(required=True), "age": fields.Int(required=True)}, location="query")
def greetings_by_query(args):  # put application's code here
    name: str = args["name"]
    age: int = args["age"]

    return f"Hi, {name}. You are {age} old."


if __name__ == "__main__":
    app.run()
