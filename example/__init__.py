import odin

from flask import Flask
from odinweb import api, doc
from odinweb.api import ApiCollection, ApiVersion
from odinweb.flask import ApiBlueprint
# from odinweb.swagger import SwaggerSpec
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

    @doc.deprecated
    @api.collection(url_path='find', methods=api.Method.POST)
    def operation_test(self, request):
        pass

    @api.listing
    def get_user_list(self, request, limit, offset):
        return [
            User(1, "tim"),
            User(2, "sara"),
        ], 2

    @api.create
    def create_user(self, request, user):
        """
        Create a new user.
        """
        user.id = 3
        return user

    @api.detail
    def get_user(self, request, resource_id):
        """
        Get a user object
        """
        return User(resource_id, "tim")

    @api.update
    def update_user(self, request, user, resource_id):
        return user

    @api.patch
    def patch_user(self, request, user, resource_id):
        return user

    @api.delete
    def delete_user(self, request, resource_id):
        return self.create_response(200)


class GroupApi(api.ResourceApi):
    resource = Group

    @api.Operation(tags=['user'])
    def list_groups(self, request):
        return []

sample_api = ApiCollection(name='sample')


@sample_api.operation(url_path='foo/bar')
def sample(request):
    return {}

app = Flask(__name__)
app.register_blueprint(
    ApiBlueprint(
        ApiVersion(
            SwaggerSpec("Flask Example Swaggerspec", enable_ui=True),
            sample_api,
            GroupApi(),
            UserApi(),
        ),
        debug_enabled=True,
    ),
)
