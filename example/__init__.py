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


@app.route("/<name>/")
def hello(name):
    return "HelloWorld! " + name


app.register_blueprint(
    api.ApiBlueprint(
        api.ApiVersion(BookApi)
    )
)
