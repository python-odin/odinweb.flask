from flask import Flask, request

from odinweb import flask
from odinweb.constants import Method
from odinweb.testing import check_request_proxy


def test_request_proxy():
    test_app = Flask(__name__)
    test_app.testing = True
    app = test_app.test_client()

    @test_app.route('/')
    def test_method():
        target = flask.RequestProxy(request)
        check_request_proxy(target)
        assert target.method == Method.GET
        return 'OK'

    rv = app.get('/?a=1&b=2&a=3')
