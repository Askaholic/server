import inspect
from functools import wraps


def get_new_args(app, spec, args):
    services = []
    for arg in spec.args:
        if arg in app._service_factories:
            services.append(app._get_service(arg))
        elif arg != 'self':
            # Stop on the first argument that is not a service
            break

    return services + list(args)


def get_inject_wrapper(app, obj):
    spec = inspect.getfullargspec(obj)

    if inspect.isclass(obj):
        return _get_class_inject_wrapper(app, spec, obj)
    else:
        return _get_function_inject_wrapper(app, spec, obj)


def _get_class_inject_wrapper(app, spec, obj):
    init = obj.__init__
    @wraps(init)
    def wrapper(self, *args, **kwargs):
        new_args = get_new_args(app, spec, args)
        return init(self, *new_args, **kwargs)
    obj.__init__ = wrapper
    return obj


def _get_function_inject_wrapper(app, spec, obj):
    @wraps(obj)
    def wrapper(*args, **kwargs):
        new_args = get_new_args(app, spec, args)
        return obj(*new_args, **kwargs)

    return wrapper
