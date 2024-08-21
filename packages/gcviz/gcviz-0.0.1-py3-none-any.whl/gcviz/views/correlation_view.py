import logging
from datetime import datetime

import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html

import gcviz.defaults as defaults
import gcviz.stats as stats
from gcviz.components import CompoundDropdown
from gcviz.netcdf import GlobalLoader
from gcviz.stats import Statistics, apply_statistics
from gcviz.view import View

logger = logging.getLogger("gcviz.views.correlation_view")
loader = GlobalLoader.get()

correlation_graph = View(
    name="correlation graph",
    dash_component=html.Div(
        [
            html.Div(
                [
                    html.A("Reference compound:"),
                    CompoundDropdown(
                        id="dropdown-refcompound",
                        value="cfc-12",
                    ),
                ],
                style={"display": "flex", "flexWrap": "wrap"},
            ),
            dcc.Graph(id="graph-correlation"),
        ]
    ),
)


@callback(
    Output("graph-correlation", "figure"),
    Input("ploting-button", "n_clicks"),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
    State("dropdown-compounds", "value"),
    State("dropdown-refcompound", "value"),
    State("dropdown-symbols", "value"),
    State("checklist-sites", "value"),
    State("checklist-flags", "value"),
    State("dropdown-datastatistics", "value"),
    State("dropdown-scatter-mode", "value"),
    prevent_initial_call=True,
)
def update_correlation_plot(
    n_clicks,
    start_date,
    end_date,
    selected_compound,
    reference_compound,
    symbol,
    selected_sites,
    flags,
    statistics,
    scatter_mode,
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

        read_kwargs = {
            "site": site,
            "date_interval": dt_interval,
            "pollution_removed": "remove pollution" in flags,
            "met_office_only": "only metoffice baseline" in flags,
        }

        serie = loader.read_data(compound=selected_compound, **read_kwargs)
        serie_ref = loader.read_data(compound=reference_compound, **read_kwargs)

        if serie is None:
            logger.debug(f"No data found for {site=} {selected_compound=}")
            continue
        if serie_ref is None:
            logger.debug(f"No data found for {site=} {reference_compound=}")
            continue

        serie = apply_statistics(serie, Statistics(statistics))
        serie_ref = apply_statistics(serie_ref, Statistics(statistics))

        # Keep only the common index
        serie = serie[serie.index.isin(serie_ref.index)]
        serie_ref = serie_ref[serie_ref.index.isin(serie.index)]

        fig.add_trace(
            go.Scatter(
                x=serie_ref.values,
                y=serie.values,
                mode=scatter_mode,
                marker_symbol=symbol,
                marker_color=defaults.sites_colors.get(site, "black"),
                name=site,
            )
        )

    fig.update_layout(
        xaxis_title=f"concentration of {reference_compound} [ppt]",
        yaxis_title=f"concentration of {selected_compound} [ppt]",
    )
    logger.info(f"Figure Ready")
    return fig
