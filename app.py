import random

from faker import Faker
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from application.services import generate_humans
from application.typing import T_ITERATOR_WITH_INTEGERS

app = Flask(__name__)
faker = Faker("uk_UA")


def get_items_as_iterator(amount: int = 20) -> T_ITERATOR_WITH_INTEGERS:
    return (random.randint(0, 100) for _ in range(amount))


@app.route("/")
def hello_world():
    return "Hello World! 13"


@app.route("/generate-humans")
@use_args({"amount": fields.Int(missing=3)}, location="query")
def generate_humans_view(args):
    humans_amount = args["amount"]

    list_items_formatted = "".join(
        f"<li>{human.name} - {human.age}</li>" for human in generate_humans(amount=humans_amount)
    )
    return f"<ol>{list_items_formatted}</ol>"


@app.route("/generate-humans-2")
@app.route("/generate-humans-2/<int:amount>")
def generate_humans_view_2(amount: int = 7):
    humans_amount = amount

    list_items_formatted = "".join(
        f"<li>{human.name} - {human.age}</li>" for human in generate_humans(amount=humans_amount)
    )
    return f"<ol>{list_items_formatted}</ol>"


@app.route("/example")
def example():
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
def greetings_by_path(name: str, age: int):
    return f"Hi, {name}. You are {age} old."


@app.route("/greetings-2")
@use_args({"name": fields.Str(required=True), "age": fields.Int(required=True)}, location="query")
def greetings_by_query(args):
    name: str = args["name"]
    age: int = args["age"]

    return f"Hi, {name}. You are {age} old."


if __name__ == "__main__":
    app.run()
