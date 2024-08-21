from gcviz.layout.sites_selection import create_site_selection

from datetime import date
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback, dash_table, dcc, html

from gcviz.view import View
from gcviz.components import CompoundDropdown
from gcviz.stats import Statistics
import gcviz.style as style


def create_selection_bar(
    views: list[View], sites: list[str], config: dict[str, any]
) -> list[html.Div]:

    view_selection = dbc.DropdownMenu(
        children=dcc.Checklist(
            [
                {
                    "label": html.Div([view.name]),
                    "value": view.name,
                }
                for view in views
            ],
            value=[view.name for view in views],
            labelStyle={"display": "flex"},
            id="checklist-views",
        ),
        label="Views",
        id="dropdown-views",
    )

    layout = html.Div(
        [
            view_selection,
            create_site_selection(sites),
            CompoundDropdown(id="dropdown-compounds", value="cfc-11"),
            dcc.DatePickerRange(
                id="date-range",
                start_date=date(1980, 1, 1),
                end_date_placeholder_text="End Period",
                display_format="YYYY-MM",
                clearable=True,
            ),
            dbc.DropdownMenu(
                children=dcc.Checklist(
                    [
                        {"label": html.Div([flag]), "value": flag}
                        for flag in [
                            "remove pollution",
                            "only metoffice baseline",
                        ]
                    ],
                    value=[],
                    labelStyle={"display": "flex"},
                    id="checklist-flags",
                ),
                label="Flags",
                id="dropdown-flags",
            ),
            dcc.Dropdown(
                id="dropdown-symbols",
                options=style.symbols,
                value="cross",
                style={"width": "100px"},
                clearable=False,
            ),
            dcc.Dropdown(
                id="dropdown-scatter-mode",
                options=style.scatter_modes,
                value="markers",
                style={"width": "150px"},
                clearable=False,
            ),
            dcc.Dropdown(
                id="dropdown-datastatistics",
                options=[stat.value for stat in Statistics],
                value=Statistics.MEAN_MOUNTHS.value,
                style={"width": "150px"},
                clearable=False,
            ),
            dcc.Checklist(
                [{"label": "baseline", "value": "baseline"}],
                value=[],
                labelStyle={"display": "flex"},
                id="checklist-baseline",
            ),
            # Button that triggers the plot
            dbc.Button("plot", id="ploting-button"),
            # Sipmple text
            html.Div(id="selecteddata-text"),
        ],
        style={"display": "flex", "flexWrap": "wrap"},
    )

    @callback(
        Output("selecteddata-text", "children"),
        Input("graph-content", "clickData"),
    )
    def update_selected_data(clickData):
        if clickData is None:
            return "No data selected"
        datapoint = clickData["points"][0]
        return f"Selected data: {datapoint['x']}, {datapoint['y']:0.2f}"

    @callback(
        Output("checklist-sites", "value"),
        Input("checklist-sites-all", "value"),
        prevent_initial_call=True,
    )
    def select_all_sites(all_sites):
        if "all_sites" in all_sites:
            return sites
        return []

    for view in views:
        # Enable or disable the views
        @callback(
            Output(component_id=view.id, component_property="style"),
            Input(component_id="checklist-views", component_property="value"),
        )
        def show_hide_view(selected_view, view=view):
            if view.name in selected_view:
                return {"display": "block"}
            return {"display": "none"}

    return layout
