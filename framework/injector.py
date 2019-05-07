import inspect
from functools import wraps
from typing import Any, Callable, List, Tuple


def get_inject_wrapper(app, obj: Callable[..., Any]) -> Callable[..., Any]:
    spec = inspect.getfullargspec(obj)

    if inspect.isclass(obj):
        return _get_class_inject_wrapper(app, spec, obj)
    else:
        return _get_function_inject_wrapper(app, spec, obj)


def _get_class_inject_wrapper(app, spec, obj: Callable[..., Any]) -> Callable[..., Any]:
    init = obj.__init__
    @wraps(init)
    def wrapper(self, *args, **kwargs):
        new_args = get_new_args(app, spec, args)
        return init(self, *new_args, **kwargs)
    obj.__init__ = wrapper
    return obj


def _get_function_inject_wrapper(app, spec, obj: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(obj)
    def wrapper(*args, **kwargs):
        new_args = get_new_args(app, spec, args)
        return obj(*new_args, **kwargs)

    return wrapper


def get_new_args(app, spec, args: Tuple[Any, ...]) -> List[Any]:
    services = []
    for arg in spec.args:
        if arg in app._service_factories:
            services.append(app._get_service(arg))
        elif arg != 'self':
            # Stop on the first argument that is not a service
            break

    return services + list(args)
