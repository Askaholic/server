import pytest
from server.router import Router, route


async def test_router():
    class SomeProtocol(Router):
        def __init__(self, arg: str, kwarg: int=0):
            pass

        @route("Command")
        async def handler(self, arg1: int, arg2: int):
            return arg1 - arg2

        def some_function(self, a: int):
            return a + 1

    proto = SomeProtocol("Hello", kwarg=100)

    assert await proto.handle_command("Command", 23, -19) == 42
    assert await proto.handler(23, -19) == 42
    assert proto.some_function(1) == 2


async def test_router_module():
    pytest.skip("Need to rework module system first")

    class SomeModule(Router):
        @route("ModuleCommand")
        async def handler(self, arg1: int, arg2: str):
            return f"{arg2}: {arg1}"

        @route("BaseCommand")
        async def base_handler(self):
            return 999

    class SomeProtocol(Router):
        modules = [
            SomeModule
        ]

        @route("Command")
        async def handler(self):
            return 42

        @route("BaseCommand")
        async def base_handler(self):
            return 7

    proto = SomeProtocol()

    assert await proto.handle_command("Command") == 42
    assert await proto.handle_command("ModuleCommand", 3, "I am") == "I am: 3"
    assert await proto.handle_command("BaseCommand") == 999


async def test_route_matching():
    class SomeProtocol(Router):
        def __init__(self):
            self.num = 0

        @route("Command")
        async def command(self):
            return 42

        @route("Command", action="add")
        async def command_add(self, message):
            self.num += message['num']

        @route("Command", action="sub")
        async def command_sub(self, message):
            self.num -= message['num']

    proto = SomeProtocol()

    await proto.handle_command({"command": "Command", "action": "add"}, {"num": 1})
    assert proto.num == 1

    await proto.handle_command({"command": "Command", "action": "sub"}, {"num": 2})
    assert proto.num == -1

    assert await proto.handle_command({"command": "Command", "action": "other"}) == 42
    assert await proto.handle_command("Command") == 42


async def test_multi_route():
    class SomeProtocol(Router):
        def __init__(self):
            self.num = 0

        @route("Command", action="add")
        @route("Command", action="other_add")
        @route("DeprecatedCommand")
        async def command_add(self, message):
            self.num += message['num']

    proto = SomeProtocol()

    await proto.handle_command({"command": "Command", "action": "add"}, {"num": 1})
    assert proto.num == 1
    await proto.handle_command({"command": "Command", "action": "other_add"}, {"num": 2})
    assert proto.num == 3
    await proto.handle_command({"command": "DeprecatedCommand"}, {"num": 39})
    assert proto.num == 42
