"""Custom Dash components"""

from dash import dcc

from gcviz.netcdf import GlobalLoader


class CompoundDropdown(dcc.Dropdown):
    """A dropdown for selecting compounds."""

    def __init__(self, **kwargs):
        loader = GlobalLoader.get()
        kwargs["options"] = sorted(loader.compounds)
        if "value" not in kwargs:
            kwargs["value"] = loader.compounds[0]
        kwargs["searchable"] = True
        kwargs["clearable"] = False
        # Make it long enough to see long compound names
        kwargs["style"] = {"width": "200px"}
        super().__init__(**kwargs)
