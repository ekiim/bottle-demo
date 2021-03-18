import json
import bottle

app = bottle.Bottle()

@app.route("/", method=["GET"])
def index():
    return {"status": "OK"}

@app.route("/contact", method=["POST"])
def get_contacts():
    formdata = bottle.request.forms
    name = formdata.get("nombre", "-")
    email = formdata.get("email", "-")
    print(name, email)
    bottle.redirect("http://0.0.0.0:8888/thanks.html")

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
    bottle.response.status = 404
    bottle.response.content_type = "application/json"
    return json.dumps({"status": "Ups"})

@app.error(405)
def error_405(error):
    bottle.response.status = 405
    bottle.response.content_type = "application/json"
    return json.dumps({"status": "Accediste mal, esto no soporta el verbo http que quieres usar."})

@app.error(500)
def error_500(error):
    bottle.response.status = 500
    bottle.response.content_type = "application/json"
    return json.dumps({"status": "Super Ups"})

if __name__ == '__main__':
    print("Iniciando servidor")
    app.run(host="0.0.0.0", port=9999, debug=True)
