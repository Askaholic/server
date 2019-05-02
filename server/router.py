from typing import Any, Callable, Coroutine, Dict, List, Union

TFunc = Callable[..., Any]
TCoro = Coroutine[None, List[Any], Any]
TMessage = Union[str, Dict[str, Any]]


class Route():
    def __init__(self, command: str, **kwargs):
        self.command = command
        self.kwargs = kwargs

    def matches(self, message: TMessage) -> bool:
        if isinstance(message, str):
            return message == self.command and not self.kwargs

        if 'command' not in message or message['command'] != self.command:
            return False

        return self._matches_kwargs(message)

    def _matches_kwargs(self, message: Dict[str, Any]) -> bool:
        for k, v in self.kwargs.items():
            if k not in message:
                return False

            if message[k] != v:
                return False
        return True


class RouterMeta(type):
    def __new__(mcls, name: str, bases, params):
        cls = super().__new__(mcls, name, bases, params)
        routes: List[TCoro] = []

        # Register base routes
        route_funcs = filter(lambda x: hasattr(x, "_routes"), params.values())
        for route_func in route_funcs:
            routes.append(route_func)

        # Register routes from our modules
        for mod in params.get('modules', []):
            routes += mod.routes

        cls.routes = routes
        return cls


class Router(metaclass=RouterMeta):
    routes: List[TCoro] = []  # Helps the type checker

    async def handle_command(self, message: TMessage, *args: Any):
        try:
            handler = _get_matching_route(self.__class__.routes, message)
        except KeyError:
            self._logger.exception(
                "Unrecognized command %s(%s) from %s",
                message, args, self
            )
            return

        try:
            coro = handler(self, *args)
        except (TypeError, ValueError) as e:
            self._logger.exception("Bad command arguments: %s", e)
            return

        return await coro


def route(command: str, **kwargs) -> TFunc:
    def decorator(f: TCoro) -> TCoro:
        if not hasattr(f, '_routes'):
            f._routes = []
        f._routes.append(Route(command, **kwargs))
        return f
    return decorator


def _get_matching_route(routes: List[TCoro], message: TMessage) -> TCoro:
    # Newer routes are always appended to the list, so we need to search in
    # reverse order to find the most recently defined route
    for func in reversed(routes):
        for route in func._routes:
            if route.matches(message):
                return func
    raise KeyError
