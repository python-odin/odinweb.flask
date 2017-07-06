"""
OdinWeb.Flask API
~~~~~~~~~~~~~~~~~

Flask implementation of the OdinWeb API interface.

"""
from flask import Flask
from odinweb.api import ResourceApi


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

        url_prefix = self.options.get('url_prefix')
        if url_prefix is None:
            url_prefix = self.blueprint.url_prefix

        #: The prefix that should be used for all URLs defined on the
        #: blueprint.
        self.url_prefix = url_prefix

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """A helper method to register a rule (and optionally a view function)
        to the application.  The endpoint is automatically prefixed with the
        blueprint's name.
        """
        if self.url_prefix:
            rule = self.url_prefix + rule
        options.setdefault('subdomain', self.subdomain)
        self.app.add_url_rule(rule, '%s.%s' % (self.blueprint.name, endpoint),
                              view_func, **options)

    def add_api_route(self, api_route):
        url_path_nodes = [self.url_prefix] + api_route
        url_path = '/'.join(
            str(node) if isinstance(node, tuple) else "<{0}:{1}>"
            for node in url_path_nodes
        )
        self.app


class ApiBlueprint(object):
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

    def __init__(self, *collections, **kwargs):
        self.collections = collections

        # Extract names from kwargs (this is a workaround for python 2.7)
        self.name = kwargs.pop('name', 'api')
        self.url_prefix = kwargs.pop('url_prefix', '/')
        self.subdomain = kwargs.pop('subdomain', None)

        if kwargs:
            raise TypeError("'{}' is an invalid keyword argument for this function".format(kwargs.keys()[-1]))

        self.deferred_functions = []

    def record(self, func):
        """Registers a function that is called when the blueprint is
        registered on the application.  This function is called with the
        state as argument as returned by the :meth:`make_setup_state`
        method.
        """
        if self._got_registered_once:
            from warnings import warn
            warn(Warning('The blueprint was already registered once '
                         'but is getting modified now.  These changes '
                         'will not show up.'))
        self.deferred_functions.append(func)

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

        for collection in self.collections:
            for api_route in collection.api_routes():
                state.add_api_route(api_route)

        for deferred in self.deferred_functions:
            deferred(state)
#
#
# class ApiCollection(object):
#     """
#     Collection of API endpoints
#     """
#     def __init__(self, *resource_apis, **kwargs):
#         self.api_name = kwargs.pop('api_name', 'api')
#         self.resource_apis = resource_apis
#
#     def register(self, app, prefix=None):
#         if prefix:
#             base_name = "{}/{}".format(prefix, self.api_name)
#         else:
#             base_name = self.api_name
#
#         # for resource_api in self.resource_apis:
#         #     resource_api.register(app)
#
#
# class ApiVersion(ApiCollection):
#     """
#     A versioned collection of several resource API's.
#     Along with helper methods for building URL patterns.
#     """
#     def __init__(self, *resource_apis, **kwargs):
#         kwargs.setdefault('api_name', kwargs.pop('version', 'v1'))
#         super(ApiVersion, self).__init__(*resource_apis, **kwargs)
#
#
# class Api(object):
#     """
#     An API::
#
#         from flask import Flask
#         from odinweb.flask.api import ApiBlueprint
#
#         app = Flask(__name__)
#
#         app.register_blueprint(
#             ApiBlueprint(
#                 ApiVersion(
#                     UserApi(),
#                     version='v1
#                 )
#             )
#         )
#
#     """
#     def __init__(self, *collections, **kwargs):
#         self.collections = collections
#         self.api_name = kwargs.get('api_name', 'api')
#
#     def register(self, app):
#         # type: (Flask) -> None
#         """
#         Register api with Flask.
#
#         :param app: An instance of Flask.
#
#         """
#         base_name = self.api_name
#         for collection in self.collections:
#             collection.register(app, base_name)
#         app.add_url_rule('/{}/'.format(base_name), view_func=self._unknown_version)
#         app.add_url_rule('/{}/<string:version>/'.format(base_name), view_func=self._unknown_version)
#         app.add_url_rule('/{}/<string:version>/<path:path>'.format(base_name), view_func=self._unknown_version)
#
#     def _unknown_version(self, version=None, **_):
#         return "Versions..." + str(_)
