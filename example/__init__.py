import odin

from flask import Flask
from odinweb.flask import api


app = Flask(__name__)


class Book(odin.Resource):
    title = odin.StringField()
    published = odin.DateField()
    authors = odin.TypedListField(odin.StringField())


class BookApi(api.ResourceApi):
    resource = Book


@app.route("/")
def hello():
    return "HelloWorld!"

api.Api(
    api.ApiVersion(BookApi())
).register(app)
