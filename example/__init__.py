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
    def get_user_list(self, request, limit, offset):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ]

    @detail
    def get_user(self, request, resource_id):
        return User(resource_id, "tim")


app.register_blueprint(
    ApiBlueprint(
        ApiVersion(
            UserApi()
        ),
        debug_enabled=True
    )
)
