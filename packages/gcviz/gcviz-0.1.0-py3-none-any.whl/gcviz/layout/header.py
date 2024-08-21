from dash import Dash, Input, Output, State, callback, dash_table, dcc, html
import dash_bootstrap_components as dbc


def create_header():
    title = html.H1(children="gcviz", style={"textAlign": "center"})
    dev_alert = dbc.Container(
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
    )
    return html.Div([title, dev_alert])
