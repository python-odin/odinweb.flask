from odinweb import flask
from odinweb.testing import check_request_proxy


def test_request_proxy():
    check_request_proxy(flask.RequestProxy)
