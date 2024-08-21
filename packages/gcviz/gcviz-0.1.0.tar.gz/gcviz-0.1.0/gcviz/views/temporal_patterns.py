from datetime import datetime
import logging

import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html

import gcviz.defaults as defaults
import gcviz.stats as stats
from gcviz.components import CompoundDropdown
from gcviz.stats import Statistics, TimeAverageType, apply_statistics, fit_baseline
from gcviz.view import View
from gcviz.netcdf import GlobalLoader


logger = logging.getLogger("gcviz.views.base_figures")
loader = GlobalLoader.get()

temporal_patterns = View(
    name="temporal patterns",
    dash_component=html.Div(
        [
            html.Div(
                [
                    html.A("Temporal Pattern"),
                    dcc.Dropdown(
                        id="dropdown-temporalpatterns",
                        value=TimeAverageType.MONTH_OF_YEAR.value,
                        options=[
                            {"label": avg_type.value, "value": avg_type.value}
                            for avg_type in TimeAverageType
                        ],
                        style={"width": "200px"},
                    ),
                ],
                style={"display": "flex", "flexWrap": "wrap"},
            ),
            dcc.Graph(id="graph-temporalpatterns"),
        ]
    ),
)


@callback(
    Output("graph-temporalpatterns", "figure"),
    Input("ploting-button", "n_clicks"),
    Input("dropdown-temporalpatterns", "value"),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
    State("dropdown-compounds", "value"),
    State("checklist-sites", "value"),
    State("checklist-flags", "value"),
    prevent_initial_call=True,
)
def update_graph_temporalpatterns(
    n_clicks,
    temporal_pattern,
    start_date,
    end_date,
    selected_compound,
    selected_sites,
    flags,
):

    temporal_pattern = TimeAverageType(temporal_pattern)
    logger.info(
        f"Plotting temporal patterns for {selected_compound=} with {temporal_pattern=}"
    )

    dt_interval = (
        datetime.strptime(start_date, "%Y-%m-%d") if start_date else None,
        datetime.strptime(end_date, "%Y-%m-%d") if end_date else None,
    )
    fig = go.Figure()

    # A little offset to separate the sites
    site_offset = iter(np.linspace(0, 0.5, len(selected_sites) + 1))

    for site in selected_sites:

        serie = loader.read_data(
            site,
            selected_compound,
            date_interval=dt_interval,
            pollution_removed="remove pollution" in flags,
            met_office_only="only metoffice baseline" in flags,
        )

        if serie is None:
            logger.debug(f"No data found for {site=} {selected_compound=}")
            continue

        # Group the data by the temporal value selected
        groupped = serie.groupby(
            getattr(serie.index, stats.groupping.get(temporal_pattern))
        )
        mean = groupped.mean()
        std = groupped.std()

        fig.add_trace(
            go.Scatter(
                x=mean.index + next(site_offset),
                y=mean.values,
                error_y=dict(
                    type="data",
                    array=std.values,
                    visible=True,
                ),
                name=site,
                marker_color=defaults.sites_colors.get(site, "black"),
            )
        )

    ticks = stats.x_ticks[temporal_pattern]
    fig.update_layout(
        xaxis_title=temporal_pattern.value,
        yaxis_title=f"Average and std for concentration of {selected_compound} [ppt]",
        xaxis=dict(
            tickmode="array",
            tickvals=list(ticks.keys()),
            ticktext=list(ticks.values()),
        ),
    )
    logger.info(f"Figure Ready")
    return fig
