"""
OdinWeb.Flask API
~~~~~~~~~~~~~~~~~

Flask implementation of the OdinWeb API interface.

"""
from __future__ import absolute_import

from flask import Flask, request, make_response
from odinweb.data_structures import ApiBase, PathNode


class ApiBlueprintSetupState(object):
    """Temporary holder object for registering a blueprint with the
    application.  An instance of this class is created by the
    :meth:`~flask.Blueprint.make_setup_state` method and later passed
    to all register callback functions.
    """

    def __init__(self, blueprint, app, options, first_registration):
        #: a reference to the current application
        self.app = app

        #: a reference to the blueprint that created this setup state.
        self.blueprint = blueprint

        #: a dictionary with all options that were passed to the
        #: :meth:`~flask.Flask.register_blueprint` method.
        self.options = options

        #: as blueprints can be registered multiple times with the
        #: application and not everything wants to be registered
        #: multiple times on it, this attribute can be used to figure
        #: out if the blueprint was registered in the past already.
        self.first_registration = first_registration

        subdomain = self.options.get('subdomain')
        if subdomain is None:
            subdomain = self.blueprint.subdomain

        #: The subdomain that the blueprint should be active for, ``None``
        #: otherwise.
        self.subdomain = subdomain

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """A helper method to register a rule (and optionally a view function)
        to the application.  The endpoint is automatically prefixed with the
        blueprint's name.
        """
        options.setdefault('subdomain', self.subdomain)
        self.app.add_url_rule(rule, '%s.%s' % (self.blueprint.name, endpoint), view_func, **options)


class ApiBlueprint(ApiBase):
    """
    A Flask Blueprint for an API::

        from flask import Flask
        from odinweb.flask.api import ApiBlueprint

        app = Flask(__name__)

        app.register_blueprint(
            ApiBlueprint(
                ApiVersion(
                    UserApi(),
                    version='v1
                )
            )
        )

    """
    _got_registered_once = False

    def __init__(self, *endpoints, **options):
        self.subdomain = options.pop('subdomain', None)
        super(ApiBlueprint, self).__init__(*endpoints, **options)

    def parse_node(self, node):
        if isinstance(node, PathNode):
            if node.type_args:
                return "<{}({}):{}>".format(node.type, ', '.join(node.type_args), node.name)
            else:
                return "<{}:{}>".format(node.type, node.name)
        else:
            return str(node)

    def _bound_callback(self, f):
        def callback(**kwargs):
            response = make_response(f(request, **kwargs))

            # Todo: Deal with response object and map back to Bottle.response
            response.headers['content-type'] = 'text/plain'

            return response
        return callback

    def make_setup_state(self, app, options, first_registration=False):
        # type: (Flask, dict, bool) -> ApiBlueprintSetupState
        """Creates an instance of :meth:`~flask.blueprints.BlueprintSetupState`
        object that is later passed to the register callback functions.
        Subclasses can override this to return a subclass of the setup state.
        """
        return ApiBlueprintSetupState(self, app, options, first_registration)

    def register(self, app, options, first_registration):
        # type: (Flask, dict, bool) -> None
        """
        Register interface

        :param app: Instance of flask.
        :param options: Options for blueprint
        :param first_registration: First registration of blueprint

        """
        self._got_registered_once = True
        state = self.make_setup_state(app, options, first_registration)

        for path, methods, callback in super(ApiBlueprint, self)._build_routes():
            state.add_url_rule(path, path, self._bound_callback(callback), methods=methods)
