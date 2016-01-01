from flask import Flask
print(__name__)
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/test")
def test():
    return "testing shit!"


if __name__ == "__main__":
    app.run()