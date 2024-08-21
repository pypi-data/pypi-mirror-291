import json
import logging
import importlib
import argparse

from datetime import date, datetime
from pathlib import Path

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, callback, dash_table, dcc, html


from gcviz.components import CompoundDropdown
import gcviz.defaults as defaults
from gcviz.config import GlobalConfig
import gcviz.stats as stats
import gcviz.style as style
from gcviz.netcdf import NetcdfLoader, GlobalLoader
from gcviz.stats import Statistics, TimeAverageType, apply_statistics, fit_baseline

from gcviz.view import View


# Read the arguments
parser = argparse.ArgumentParser(description="gcviz")

# Make it the first argument
parser.add_argument(
    "--config",
    type=str,
    default="run_config.json",
    help="The path to the config file",
)

args = parser.parse_args()

# Read the config
config_path = Path(args.config)
if not config_path.exists():
    raise FileNotFoundError(
        f"Config file not found: {config_path}. Please provide a valid path."
    )


with open(config_path) as f:
    config = json.load(f)

assert isinstance(config, dict)

GlobalConfig.set(config)
data_config = config.get("data", {})


# Setup the logging
log_level = config.get("logging", {}).get("level", "INFO")
logger = logging.getLogger("gcviz.app")
logging.basicConfig(level=getattr(logging, log_level))

# Look at the data
loader = NetcdfLoader(
    directory=config["netcdf_directory"],
    invalid_value=data_config.get("invalid_value", None),
)
GlobalLoader.set(loader)


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# Import the view form the config
views = [
    # Import as specified in the config
    getattr(importlib.import_module(f"gcviz.views.{view_file}"), view_variable)
    for view_variable, view_file in config.get("views", {}).items()
]


layout = [
    html.H1(children="gcviz", style={"textAlign": "center"}),
    dbc.Container(
        dbc.Alert(
            html.Div(
                [
                    html.A(
                        "This is currently in developpement. If you have a problem, please report on "
                    ),
                    html.A(
                        "our Gitlab",
                        href="https://gitlab.com/empa503/atmospheric-measurements/gcviz/-/issues",
                    ),
                ]
            ),
            color="info",
        ),
        class_name="developpement-alert",
    ),
    html.Div(
        [
            dbc.DropdownMenu(
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
            ),
            dbc.DropdownMenu(
                children=[
                    dcc.Checklist(
                        [
                            {
                                "label": html.Div(["Tick/Untick all sites"]),
                                "value": "all_sites",
                            },
                        ],
                        value=[],
                        labelStyle={"display": "flex"},
                        id="checklist-sites-all",
                    ),
                    dcc.Checklist(
                        [
                            {
                                "label": html.Div(
                                    [site],
                                    style={
                                        "color": defaults.sites_colors.get(
                                            site, "black"
                                        )
                                    },
                                ),
                                "value": site,
                            }
                            for site in loader.sites
                        ],
                        value=["GSN", "JFJ"],
                        labelStyle={"display": "flex"},
                        id="checklist-sites",
                    ),
                ],
                label="sites",
                id="dropdown-sites",
            ),
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
    ),
    # dcc.DatePickerRange(id="date-range"),
] + [view.div for view in views]
app.layout = layout


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
        return loader.sites
    return []


for view in views:
    # Enable or disable the views
    @app.callback(
        Output(component_id=view.id, component_property="style"),
        Input(component_id="checklist-views", component_property="value"),
    )
    def show_hide_view(selected_view, view=view):
        if view.name in selected_view:
            return {"display": "block"}
        return {"display": "none"}


if __name__ == "__main__":
    app.run(
        debug=True,
        host=config.get("newtork", {}).get("host", "127.0.0.1"),
        port=config.get("newtork", {}).get("port", 8050),
    )
