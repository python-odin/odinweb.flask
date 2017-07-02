from flask import Flask


class ApiCollection(object):
    """
    Collection of API endpoints
    """
    def __init__(self, *resource_apis, **kwargs):
        self.api_name = kwargs.pop('api_name', 'api')
        self.resource_apis = resource_apis

    def register(self, app, prefix=None):
        if prefix:
            base_name = "{}/{}".format(prefix, self.api_name)
        else:
            base_name = self.api_name

        for resource_api in self.resource_apis:
            resource_api.register(app)


class ApiVersion(ApiCollection):
    """
    A versioned collection of several resource API's.
    Along with helper methods for building URL patterns.
    """
    def __init__(self, *resource_apis, **kwargs):
        kwargs.setdefault('api_name', kwargs.pop('version', 'v1'))
        super(ApiVersion, self).__init__(*resource_apis, **kwargs)


class Api(object):
    """
    An API::
        
        from flask import Flask
        from odinweb.flask.api import Api
        
        app = Flask(__name__)
    
        Api(
            ApiVersion(
                UserApi(),
                version='v1
            )
        ).register(app)
        
    """
    def __init__(self, *collections, **kwargs):
        self.collections = collections
        self.api_name = kwargs.get('api_name', 'api')

    def register(self, app):
        # type: (Flask) -> None
        """
        Register api with Flask. 

        :param app: An instance of Flask.
         
        """
        base_name = self.api_name
        for collection in self.collections:
            collection.register(app, base_name)
        app.add_url_rule('/{}/'.format(base_name), view_func=self._unknown_version)
        app.add_url_rule('/{}/<string:version>/'.format(base_name), view_func=self._unknown_version)
        app.add_url_rule('/{}/<string:version>/<path:path>'.format(base_name), view_func=self._unknown_version)

    def _unknown_version(self, version=None, **_):
        return "Versions..." + str(_)
