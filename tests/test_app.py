from data.app import app
from dash import html, dcc


def find_components_recursive(component, component_type):
    found = []

    if isinstance(component, component_type):
        found.append(component)

    if hasattr(component, 'children'):
        children = component.children
        if children is not None:
            # Handle both single child and list of children
            if not isinstance(children, list):
                children = [children]

            for child in children:
                found.extend(find_components_recursive(child, component_type))

    return found


def test_header_is_present():
    layout = app.layout
    headers = find_components_recursive(layout, html.H1)
    assert len(headers) > 0


def test_visualisation_is_present():
    layout = app.layout
    graphs = find_components_recursive(layout, dcc.Graph)
    assert len(graphs) > 0


def test_region_picker_is_present():
    layout = app.layout
    radios = find_components_recursive(layout, dcc.RadioItems)
    assert len(radios) > 0