from flask import Flask
from odinweb.flask import api

app = Flask(__name__)


@app.route("/")
def hello():
    return "HelloWorld!"

api.Api(
    api.ApiVersion()
).register(app)
