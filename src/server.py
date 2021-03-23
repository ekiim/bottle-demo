from time import time
from pathlib import Path
from os import environ
import json
import bottle

app = bottle.Bottle()

@app.route("/", method=["GET"])
def index():
    return {"status": "OK"}

def store_contact(name, email):
    data = dict(name=name, email=email)
    filename = f"{time()}.json"
    file = Path(environ["STORAGE_DIR"]) / filename
    data_string = json.dumps(data)
    file.write_text(data_string)

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
