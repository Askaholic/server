from framework import App


def test_app():
    app = App()

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


def test_nested_dependency():
    app = App()

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
