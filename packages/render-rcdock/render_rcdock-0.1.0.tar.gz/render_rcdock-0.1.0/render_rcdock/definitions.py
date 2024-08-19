# AUTO GENERATED FILE - DO NOT EDIT!

from render import Component, create_callback


class DockLayout(Component):
    Module = "rcdock"
    JSXName = "DockLayout"
    REF_HOOK = "ref"
    CALLBACKS = ["onKeyPress", "onClick"]
    ATTRIBUTES = ["style", "className", "id", "defaultLayout"]

    def __init__(
        self,
        children=None,
        key=None,
        style=None,
        className=None,
        id=None,
        onKeyPress=None,
        onClick=None,
        defaultLayout=None,
        controller=None,
    ):
        super().__init__(key, controller, children)
        self.style = style
        self.className = className
        self.id = id
        self.onKeyPress = create_callback(onKeyPress, "onKeyPress")
        self.onClick = create_callback(onClick, "onClick")
        self.defaultLayout = defaultLayout

    async def dockMove(self, *args):
        return await self.call_method("dockMove", args)

    async def saveLayout(self, *args):
        return await self.call_method("saveLayout", args)

    async def loadLayout(self, *args):
        return await self.call_method("loadLayout", args)
