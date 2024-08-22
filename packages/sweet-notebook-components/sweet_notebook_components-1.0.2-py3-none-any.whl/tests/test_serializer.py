from sweet_notebook_components.component import Text
from sweet_notebook_components.serializer import Serializer


def test_serialize_text_component() -> dict:
    text_component = Text("Hello, World!")

    serializer = Serializer()

    json = serializer.serialize_to_json(text_component)

    assert (
        json
        == """{
  "children": [],
  "props": {
    "body": "Hello, World!",
    "help": null
  },
  "type": "text"
}"""
    )
