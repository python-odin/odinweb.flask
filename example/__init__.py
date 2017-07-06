import odin

from flask import Flask
from odinweb.api import ResourceApi, ApiVersion, detail, listing
from odinweb.flask import ApiBlueprint

app = Flask(__name__)


class User(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField()


class UserApi(ResourceApi):
    resource = User

    @listing
    def get_user_list(self):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ]

    @detail
    def get_user(self, resource_id):
        return User(1, "tim")


@app.route("/<name>/")
def hello(name):
    return "HelloWorld! " + name


def sample_callback(request, **kwargs):
    return "Response: {}\n{}\n{}".format(request.path, kwargs, request.method)

app.register_blueprint(
    ApiBlueprint(
        ApiVersion(
            UserApi()
        )
    )
)
