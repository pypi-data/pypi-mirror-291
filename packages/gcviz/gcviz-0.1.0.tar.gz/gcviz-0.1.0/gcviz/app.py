import importlib
import logging

import dash_bootstrap_components as dbc
from dash import Dash

from gcviz.config import GlobalConfig
from gcviz.layout.header import create_header
from gcviz.layout.selection_bar import create_selection_bar
from gcviz.netcdf import GlobalLoader, NetcdfLoader
from gcviz.view import View

logger = logging.getLogger("gcviz.app")


def create_app(config: dict[str, any]) -> Dash:

    GlobalConfig.set(config)
    data_config = config.get("data", {})

    # Setup the logging
    log_level = config.get("logging", {}).get("level", "INFO")
    logging.basicConfig(level=getattr(logging, log_level))

    # Look at the data
    loader = NetcdfLoader(
        directory=config["netcdf_directory"],
        invalid_value=data_config.get("invalid_value", None),
    )
    GlobalLoader.set(loader)

    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Import the view form the config
    views: list[View] = [
        # Import as specified in the config
        getattr(importlib.import_module(f"gcviz.views.{view_file}"), view_variable)
        for view_variable, view_file in config.get("views", {}).items()
    ]

    layout = [
        create_header(),
        create_selection_bar(views, loader.sites, config),
    ] + [view.div for view in views]
    app.layout = layout

    return app
