from sweet_notebook_components import st


def test_factory_method() -> dict:
    text_component = st.text("Hello, World!")

    assert text_component.type == "text"
    assert text_component.body == "Hello, World!"
    assert text_component.help == None


def test_factory_method_with_help() -> dict:
    text_component = st.text("Hello, World!", help="This is a text component")

    assert text_component.type == "text"
    assert text_component.body == "Hello, World!"
    assert text_component.help == "This is a text component"


def test_internal_get_props_to_serialize() -> dict:
    text_component = st.text("Hello, World!", help="This is a text component")

    props = text_component.internal_get_props_to_serialize()

    assert props == {"body": "Hello, World!", "help": "This is a text component"}
