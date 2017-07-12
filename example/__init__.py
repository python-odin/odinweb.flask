import odin

from flask import Flask
from odinweb import api, doc
from odinweb.flask import ApiBlueprint
from odinweb.swagger import SwaggerSpec

app = Flask(__name__)


class User(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField()


class UserApi(api.ResourceApi):
    resource = User

    @api.listing
    @doc.operation(tags=['user'])
    def get_user_list(self, request, limit, offset):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ], 2

    @api.detail
    @doc.operation(tags=['user'])
    @doc.parameter('full', api.In.Query, type_=api.Type.Boolean)
    @doc.response(200, 'Return requested user.', User)
    def get_user(self, request, resource_id):
        """
        Get a user object
        """
        return User(resource_id, "tim")


app.register_blueprint(
    ApiBlueprint(
        api.ApiVersion(
            SwaggerSpec('Flask Example API'),  # Support for Swagger!
            api.ApiCollection(
                UserApi(),
            ),
        ),
        debug_enabled=True
    )
)
