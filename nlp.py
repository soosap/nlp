from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/abstract")
def system():
    name = 'Docker'
    mail = 'my_email@gmail.com'
    return jsonify(
        system=name,
        email=mail
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
