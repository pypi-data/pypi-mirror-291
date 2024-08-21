import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, callback, dash_table, dcc, html

import gcviz.defaults as defaults


def create_site_selection(sites: list[str]):

    return dbc.DropdownMenu(
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
                            style={"color": defaults.sites_colors.get(site, "black")},
                        ),
                        "value": site,
                    }
                    for site in sites
                ],
                value=[s for s in defaults.sites if s in sites],
                labelStyle={"display": "flex"},
                id="checklist-sites",
            ),
        ],
        label="sites",
        id="dropdown-sites",
    )
