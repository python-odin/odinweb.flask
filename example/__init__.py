import odin

from flask import Flask
from odinweb import api, doc
from odinweb.flask import ApiBlueprint
from odinweb.swagger import SwaggerSpec


class User(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField()
    role = odin.StringField(choices=('a', 'b', 'c'))


class UserApi(api.ResourceApi):
    resource = User

    @api.listing
    @doc.operation(tags=['user'])
    def get_user_list(self, request, limit, offset):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ], 2

    @api.create
    @doc.body_param(User)
    @doc.operation(tags=['user'])
    @doc.response(200, 'Return new user', User)
    def create_user(self, request):
        user = self.get_resource(request)
        user.id = 3
        return user

    @api.detail
    @doc.operation(tags=['user'])
    @doc.query_param('full', type=api.Type.Boolean)
    @doc.response(200, 'Return requested user.', User)
    def get_user(self, request, resource_id):
        """
        Get a user object
        """
        return User(resource_id, "tim")


app = Flask(__name__)
app.register_blueprint(
    ApiBlueprint(
        api.ApiVersion(
            SwaggerSpec('Flask Example API', enable_ui=True),  # Support for Swagger!
            api.ApiCollection(
                UserApi(),
            ),
        ),
        debug_enabled=True
    )
)
