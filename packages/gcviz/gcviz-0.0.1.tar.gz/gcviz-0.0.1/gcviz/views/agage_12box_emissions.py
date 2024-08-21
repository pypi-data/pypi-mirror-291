"""View for the global emissions estimate from agage.

To access them, clone the repository of https://github.com/mrghg/py12box_agage 
The data is not open sourced, so you will need to contact the authors to get access to the data.

"""

import logging
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html

from gcviz.config import GlobalConfig
from gcviz.view import View

config = GlobalConfig.get("py12box_agage")
logger = logging.getLogger("gcviz.views.emissions")

if "emissions_path" not in config:
    raise ValueError("`emissions_path` not found in the `py12box_agage` config.")
emissions_path = Path(config["emissions_path"])

py12box_agage_emissions = View(
    name="emission from agage 12 box model",
    dash_component=html.Div(
        [
            dcc.Graph(id="graph-emissions-12box"),
            dcc.Checklist(
                ["4 boxes", "Total"],
                ["4 boxes", "Total"],
                inline=True,
                id="checklist-emissions",
            ),
        ]
    ),
)

file_of_emissions = {
    "4 boxes": "Semihemispheric_monthly_emissions.csv",
    "Total": "Global_annual_emissions.csv",
}


available_subs = {f.name.lower(): f.name for f in (emissions_path / "data").iterdir()}


def read_units(file_path: Path) -> str:
    """Read the units from the file."""

    # it is in a commented line: # Units: Gg/yr
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("# Units:"):
                return line.split(":")[1].strip()
    return "unknown"


@callback(
    Output("graph-emissions-12box", "figure"),
    Input("ploting-button", "n_clicks"),
    Input("checklist-emissions", "value"),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
    State("dropdown-compounds", "value"),
    State("dropdown-symbols", "value"),
    State("checklist-sites", "value"),
    State("checklist-flags", "value"),
    State("dropdown-datastatistics", "value"),
    State("dropdown-scatter-mode", "value"),
    prevent_initial_call=True,
)
def update_emission_plot(
    n_clicks,
    selected_emissions: list[str] | None,
    start_date,
    end_date,
    sub: str,
    symbol,
    selected_sites,
    flags,
    statistics,
    scatter_mode,
):

    sub = available_subs.get(sub.lower(), sub)
    files_dir = emissions_path / "data" / sub / "outputs"
    # Handle the case of the names

    fig = go.Figure()

    if selected_emissions is None:
        return fig

    units = "undefined"
    for selected_emission in selected_emissions:

        file_path = files_dir / (f"{sub}_{file_of_emissions[selected_emission]}")
        if not file_path.exists():
            logger.error(f"File {file_path} does not exist.")
            continue
        units = read_units(file_path)
        df = pd.read_csv(file_path, comment="#")
        # Merge columns Year, Month
        df = df.set_index(pd.to_datetime(df[["Year", "Month"]].assign(Day=1)))
        df = df.loc[start_date:end_date]

        # Get the data
        x = df.index.to_numpy()
        match selected_emission:
            case "Total":
                # Plot
                y_err = df["Global_annual_emissions_1-sigma"].values
                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=df["Global_annual_emissions"].values,
                        error_y={"type": "data", "array": y_err},
                        mode=scatter_mode,
                        marker_symbol=symbol,
                        name="Total emissions",
                    )
                )

            case "4 boxes":
                for box in [0, 1, 2, 3]:
                    # Semihemispheric_annual_emissions_box0,Semihemispheric_annual_emissions_box1,Semihemispheric_annual_emissions_box2,Semihemispheric_annual_emissions_box3,Semihemispheric_annual_emissions_1-sigma_box0,Semihemispheric_annual_emissions_1-sigma_box1,Semihemispheric_annual_emissions_1-sigma_box2,Semihemispheric_annual_emissions_1-sigma_box3
                    y_err = df[
                        f"Semihemispheric_monthly_emissions_1-sigma_box{box}"
                    ].values
                    # Plot
                    fig.add_trace(
                        go.Scatter(
                            x=x,
                            y=df[f"Semihemispheric_monthly_emissions_box{box}"].values,
                            mode=scatter_mode,
                            error_y={"type": "data", "array": y_err},
                            marker_symbol=symbol,
                            name=f"box {box}",
                        )
                    )
            case _:
                logger.error(f"Emission type `{selected_emission}` not handled.")

    # Labels
    ax = fig.update_layout(
        xaxis_title="Date",
        yaxis_title=f"{sub} emissions [{units}]",
    )

    return fig
