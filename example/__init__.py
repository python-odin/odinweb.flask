import odin

from flask import Flask
from odinweb.api import ResourceApi, ApiCollection
from odinweb.data_structures import ApiRoute, PathNode
from odinweb.flask import ApiBlueprint

app = Flask(__name__)


class Book(odin.Resource):
    title = odin.StringField()
    published = odin.DateField()
    authors = odin.TypedListField(odin.StringField())


class BookApi(ResourceApi):
    resource = Book


@app.route("/<name>/")
def hello(name):
    return "HelloWorld! " + name


def sample_callback(request, **kwargs):
    return "Response: {}\n{}\n{}".format(request.path, kwargs, request.method)

app.register_blueprint(
    ApiBlueprint(
        ApiCollection(
            ApiRoute(1, ['user'], ['GET', 'POST'], sample_callback),
            ApiRoute(1, ['user', PathNode('resource_id', 'int', [])], ['GET', 'POST'], sample_callback),
        ),
        # ApiVersion(BookApi)
    )
)
