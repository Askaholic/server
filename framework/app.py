import inspect
from functools import wraps
from typing import Any, Callable, Dict


class App(object):
    """
        Does dependency injection
    """
    def __init__(self):
        # Map of service names to factories (commonly classes)
        self._service_factories: Dict[str, Callable] = {}
        self._services: Dict[str, 'Service'] = {}

    def service(self, name: str):
        """ Decorator for registering a service """

        def decorator(factory):
            self._service_factories[name] = factory
            return factory

        return decorator

    def inject(self, obj: Callable[..., Any]):
        """ Decorator for injecting services to a constructor. Note that this
        does not call the constructor, but returns a wrapper which will fill in
        the appropriate arguments.

            Service arguments must be placed before any other constructor
        arguments.

        Example:

        ```
            @app.inject
            class Object(object):
                def __init__(self, some_service, a, b=32):
                    self.test_service = some_service

            obj = Object(10, b=100)
            assert obj.some_service
        ```
        """

        spec = inspect.getfullargspec(obj)

        @wraps(obj)
        def wrapper(*args, **kwargs):
            services = []
            for arg in spec.args:
                if arg in self._service_factories:
                    services.append(self._get_service(arg))
                elif arg != 'self':
                    # Stop on the first argument that is not a service
                    break

            new_args = services + list(args)
            return obj(*new_args, **kwargs)

        return wrapper

    def _get_service(self, name: str) -> object:
        assert name in self._service_factories, \
            "Trying to get a service that doesn't exist"

        if name in self._services:
            return self._services[name]

        service = self._service_factories[name]()
        self._services[name] = service
        return service
