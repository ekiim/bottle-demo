from time import time
from datetime import datetime
from pathlib import Path
from os import environ
import json
import bottle


app = bottle.Bottle()


@app.route("/", method=["GET"])
def index():
    return {"status": "OK"}


def storage_file(collection="contact", ext="json"):
    """
    >>> storage_file(collection="users", ext="csv")
    >>> storage_file(collection="users", ext="json")
    >>> storage_file(collection="accounts", ext="json")
    """
    file_dir = Path(environ["STORAGE_DIR"]) / Path(collection)
    file_dir.mkdir(exist_ok=True)
    file = file_dir /  f"{time()}.{ext}"
    return file


def store_object(data, collection):
    file = storage_file(collection=collection)
    data_string = json.dumps(data)
    file.write_text(data_string)
    return True


def store_comment(email, text, entry):
    data = dict(email=email, comment=text, entry=entry)
    return store_object(data, f'blogComment_{entry}')


def read_comment_json(file):
    timestamp = float(file.stem)
    data = json.loads(file.read_text())
    data["datetime"] = datetime.fromtimestamp(timestamp).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    return data


def get_stored_comment(entry):
    comments_dir = Path(environ["STORAGE_DIR"]) / Path(f"blogComment_{entry}")
    returnable = []
    if comments_dir.exists():
        returnable = list(map(
            read_comment_json,
            sorted(comments_dir.iterdir(), reverse=True)
        ))
    return returnable


def store_contact(name, email):
    data = dict(name=name, email=email)
    return store_object(data, 'contact_form')


# GET /comments/00-entrada
@app.route("/comments/<entry>", method=["GET", "OPTIONS"])
def get_comments(entry=""):
    bottle.response.headers["Access-Control-Allow-Origin"] = (
        "http://0.0.0.0:8888"
    )
    bottle.response.headers["Access-Control-Allow-Methods"] = "GET"
    bottle.response.status = 200
    if bottle.request.method == "OPTIONS":
        return {}
    return dict(comments=get_stored_comment(entry))


# POST /comments
@app.route("/comments", method=["POST"])
def save_comment():
    formdata = bottle.request.forms
    blog_entry = formdata.get("blog-entry", "-")
    email = formdata.get("email", "-")
    comment = formdata.get("comment", "-")
    store_comment(email, comment, blog_entry)
    redirection_url = (
        environ["STATIC_SERVER"] + f"/blog/{blog_entry}.html"
    )
    bottle.redirect(redirection_url)


@app.route("/contact", method=["POST"])
def get_contacts():
    formdata = bottle.request.forms
    name = formdata.get("nombre", "-")
    email = formdata.get("email", "-")
    store_contact(name, email)
    redirection_url = (
        environ["STATIC_SERVER"] + "/thanks.html"
    )
    bottle.redirect(redirection_url)


@app.route("/name/<name>", method=["GET"])
def get_name(name="Mike"):
    return {
        "status": "OK",
        "name": name
    }


@app.route("/error/zero", method=["GET"])
def get_error(name="Mike"):
    value = 1 / 0
    return {"division by zero": value}


@app.error(404)
def error_404(error):
    bottle.response.status = 303
    redirect_url = environ["STATIC_SERVER"] + "/error.html"
    bottle.response.headers["Location"] = redirect_url


@app.error(405)
def error_405(error):
    bottle.response.status = 303
    redirect_url = environ["STATIC_SERVER"] + "/error.html"
    bottle.response.headers["Location"] = redirect_url


@app.error(500)
def error_500(error):
    bottle.response.status = 303
    redirect_url = environ["STATIC_SERVER"] + "/error.html"
    bottle.response.headers["Location"] = redirect_url


if __name__ == '__main__':
    print("Iniciando servidor")
    app.run(host="0.0.0.0", port=9999, debug=True)
