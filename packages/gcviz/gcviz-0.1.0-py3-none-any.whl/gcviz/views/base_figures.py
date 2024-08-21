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

timeseries = View(
    name="timeseries",
    dash_component=dcc.Graph(id="graph-content"),
)


@callback(
    Output("graph-content", "figure"),
    Input("ploting-button", "n_clicks"),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
    State("dropdown-compounds", "value"),
    State("dropdown-symbols", "value"),
    State("checklist-sites", "value"),
    State("checklist-flags", "value"),
    State("dropdown-datastatistics", "value"),
    State("dropdown-scatter-mode", "value"),
    State("checklist-baseline", "value"),
    prevent_initial_call=True,
)
def update_base_plot(
    n_clicks,
    start_date,
    end_date,
    selected_compound,
    symbol,
    selected_sites,
    flags,
    statistics,
    scatter_mode,
    baseline,
):

    logger.info(
        f"Plotting {selected_compound=} from {start_date=} to {end_date=} on {selected_sites=} with {flags=}"
    )

    dt_interval = (
        datetime.strptime(start_date, "%Y-%m-%d") if start_date else None,
        datetime.strptime(end_date, "%Y-%m-%d") if end_date else None,
    )
    fig = go.Figure()

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

        serie_to_plot = apply_statistics(serie, Statistics(statistics))

        site_color = defaults.sites_colors.get(site, "black")

        fig.add_trace(
            go.Scatter(
                x=serie_to_plot.index,
                y=serie_to_plot.values,
                mode=scatter_mode,
                marker_symbol=symbol,
                marker_color=site_color,
                name=site,
            )
        )

        if baseline:
            serie_baseline = fit_baseline(serie)
            if serie_baseline is None:
                logger.debug(f"Could not fit baseline for {site=} {selected_compound=}")
            else:
                fig.add_trace(
                    go.Scatter(
                        x=serie_baseline.index,
                        y=serie_baseline.values,
                        mode="lines",
                        marker_color=site_color,
                        name=f"{site} baseline",
                    )
                )

    fig.update_layout(
        # xaxis_title="Time",
        yaxis_title=f"concentration of {selected_compound} [ppt]",
    )
    logger.info(f"Figure Ready")
    return fig
