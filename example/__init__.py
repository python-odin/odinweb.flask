import odin

from flask import Flask
from odinweb import api, doc
from odinweb.flask import ApiBlueprint
from odinweb.swagger import SwaggerSpec


class User(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField()
    role = odin.StringField(choices=('a', 'b', 'c'))


class Group(odin.Resource):
    id = odin.IntegerField()
    name = odin.StringField()


class UserApi(api.ResourceApi):
    resource = User

    @api.listing
    def get_user_list(self, request, limit, offset):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ], 2

    @api.create(resource=User)
    def create_user(self, request, resource):
        user = self.get_resource(request)
        user.id = 3
        return user

    @api.detail
    @doc.query_param('full', type_=api.Type.Boolean)
    def get_user(self, request, resource_id):
        """
        Get a user object
        """
        return User(resource_id, "tim")


class GroupApi(api.ResourceApi):
    resource = Group

    @api.listing
    @doc.operation(tags=['user'])
    def list_groups(self):
        pass


app = Flask(__name__)
app.register_blueprint(
    ApiBlueprint(
        api.ApiVersion(
            SwaggerSpec('Flask Example API', enable_ui=True),  # Support for Swagger!
            api.ApiCollection(
                UserApi(),
            ),
        ),
        debug_enabled=True,
        url_prefix='/example'
    ),
)
