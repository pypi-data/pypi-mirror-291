from typing import List, Dict, Any
from IPython.display import display, HTML

from sweet_notebook_components.renderer import Renderer
from sweet_notebook_components.serializer import Serializer


class Component:

    def __init__(self, type):
        self.type = type
        self.children: List[Component] = []

    def text(self, body: str, help: str = None):
        component = Text(body, help)

        self.children.append(component)

        return component

    def to_html(self) -> str:
        return self.__repr_html__()

    def internal_get_props_to_serialize(self):
        return {}

    def __repr_html__(self) -> str:
        serializer = Serializer()
        json = serializer.serialize_to_json(self)

        renderer = Renderer()
        html = renderer.render_to_html(json)

        return html


class Root(Component):
    def __init__(self):
        super().__init__(type="root")

    def internal_get_props_to_serialize(self) -> Dict[str, Any]:
        return {}


class Text(Component):
    def __init__(self, body, help=None):
        super().__init__(type="text")

        self.body = body
        self.help = help

    def internal_get_props_to_serialize(self) -> Dict[str, Any]:
        return {"body": self.body, "help": self.help}
