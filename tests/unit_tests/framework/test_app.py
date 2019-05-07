from framework import App
from pytest import fixture


@fixture
def app():
    return App()


def test_app(app):
    @app.service("test_service")
    class TestService(object):
        pass

    service_instance = app._get_service("test_service")
    assert isinstance(service_instance, TestService)

    @app.inject
    def some_function(test_service, a, b=42):
        assert test_service is service_instance
        assert a == 10
        assert b == 42

    @app.inject
    class Object(object):
        def __init__(self, test_service, a, b=32):
            self.asdf = "asdf"
            assert test_service is service_instance
            assert a == 11
            assert b == 32

    @app.service("other_service")
    @app.inject
    class OtherService(object):
        def __init__(self, test_service):
            assert test_service is service_instance

    some_function(10)
    other = Object(11)
    assert other.asdf == "asdf"
    OtherService()


def test_nested_dependency(app):
    @app.service("test_service")
    class TestService(object):
        pass

    @app.service("middle_service")
    @app.inject
    class MiddleService(object):
        def __init__(self, test_service):
            pass

    @app.service("top_service")
    @app.inject
    class TopService(object):
        def __init__(self, middle_service):
            pass

    ts = TopService()


def test_inject_class(app):
    @app.inject
    class SomeClass(object):
        some_cls_attr = 10

        def some_method(self):
            pass

    @app.inject
    class SomeOtherClass(object):
        pass

    obj = SomeClass()
    obj.some_method()
    assert SomeClass.some_cls_attr == 10
    assert isinstance(obj, SomeClass)
    assert not isinstance(obj, SomeOtherClass)
