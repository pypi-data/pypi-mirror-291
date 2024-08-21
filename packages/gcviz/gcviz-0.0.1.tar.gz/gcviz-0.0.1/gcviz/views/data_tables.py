from dash import dash_table, callback, Output, Input

from gcviz.view import View
from gcviz import style

from gcviz.netcdf import GlobalLoader

loader = GlobalLoader.get()

all_data_table = View(
    name="all data table",
    dash_component=dash_table.DataTable(
        data=loader.df_files[style.table_columns].to_dict("records"),
        page_size=10,
        id="table-alldatafiles",
    ),
)


selected_data_table = View(
    name="selected data table",
    dash_component=dash_table.DataTable(
        page_size=10,
        id="table-datafiles",
    ),
)


# Update the datafiles table
@callback(
    Output("table-datafiles", "data"),
    Input("dropdown-compounds", "value"),
    Input("checklist-sites", "value"),
)
def update_datafiles_table(selected_compound, sites):
    df = loader.df_files[loader.df_files["compound"] == selected_compound]
    df = df[df["site"].isin(sites)]
    return df[style.table_columns].to_dict("records")
