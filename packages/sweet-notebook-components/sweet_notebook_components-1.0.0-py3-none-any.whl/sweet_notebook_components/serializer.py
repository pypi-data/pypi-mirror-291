import json
from typing import Dict, Any


class Serializer:
    def serialize_to_json(self, component) -> str:
        return json.dumps(self.__serialize_component(component), indent=2)

    def __serialize_component(self, component) -> Dict[str, Any]:
        serialized_children = [
            self.__serialize_component(child) for child in component.children
        ]

        return {
            "children": serialized_children,
            "props": component.internal_get_props_to_serialize(),
            "type": component.type,
        }
