from gcviz.view import View
from dash import html

example_view = View(
    name="example",
    dash_component=html.Div(
        [
            html.H1("Example"),
            html.P("This is an example view."),
        ],
    ),
)
