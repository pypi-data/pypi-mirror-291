from dataclasses import dataclass

from dash import html
from dash.development.base_component import Component


@dataclass
class View:

    name: str
    dash_component: Component

    def __post_init__(self):
        self.id = f"div-{self.name}"
        self.div = html.Div([self.dash_component], id=self.id)
