from flask import Flask, Response
from webargs import fields
from webargs.flaskparser import use_args

from application.services import generate_humans
from application.services.create_table import create_table
from application.services.db_connection import DBConnection
from application.services.get_items_as_iterator import get_items_as_iterator

app = Flask(__name__)


@app.route("/users/create")
@use_args({"name": fields.Str(required=True), "age": fields.Int(required=True)}, location="query")
def users__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO users (name, age) VALUES (:name, :age);",
                {"name": args["name"], "age": args["age"]},
            )

    return "Ok"


@app.route("/users/read-all")
def users__read_all():
    with DBConnection() as connection:
        users = connection.execute("SELECT * FROM users;").fetchall()

    return "<br>".join([f'{user["pk"]}: {user["name"]} - {user["age"]}' for user in users])


@app.route("/users/read/<int:pk>")
def users__read(pk: int):
    with DBConnection() as connection:
        user = connection.execute(
            "SELECT * " "FROM users " "WHERE (pk=:pk);",
            {
                "pk": pk,
            },
        ).fetchone()

    return f'{user["pk"]}: {user["name"]} - {user["age"]}'


@app.route("/users/update/<int:pk>")
@use_args({"age": fields.Int(), "name": fields.Str()}, location="query")
def users__update(
    args,
    pk: int,
):
    with DBConnection() as connection:
        with connection:
            name = args.get("name")
            age = args.get("age")
            if name is None and age is None:
                return Response(
                    "Need to provide at least one argument",
                    status=400,
                )

            args_for_request = []
            if name is not None:
                args_for_request.append("name=:name")
            if age is not None:
                args_for_request.append("age=:age")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE users " f"SET {args_2} " "WHERE pk=:pk;",
                {
                    "pk": pk,
                    "age": age,
                    "name": name,
                },
            )

    return "Ok"


@app.route("/users/delete/<int:pk>")
def users__delete(pk):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM users " "WHERE (pk=:pk);",
                {
                    "pk": pk,
                },
            )

    return "Ok"


@app.route("/")
def hello_world():
    return "Hello World!"


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


create_table()

if __name__ == "__main__":
    app.run()
