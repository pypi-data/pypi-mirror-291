# gcviz

Gorgeous and Captivating Visualization of air measurements data.

## Description

This project aims to provide a user-friendly interface to visualize air measurements data. The data is collected from various sources and is stored in a database as netcdf files.
The user can select the data source, the time period, and the type of visualization. The app will then display the data in an interactive and visually appealing way.

## Features

The concept of different `Views` makes it easy to switch between different visualizations and to implement new ones.
This makes gcviz a flexible tool that can be adapted to different needs.


## Installation

### From PyPi

To install the package from PyPi, run the following command:

```bash
pip install gcviz
```

### From source

This is the recommended way if you want to contribute to the project.

First download the repository locally.

Then make sure you have python installed.


To install the required packages, run the following command:

```bash
pip install  -e .
```

This will install the package in editable mode, so you can make changes to the code and see the changes immediately.

## Get the files 

If you don't have a specific database to plot, a good start would be the AGAGE data archive, which 
is freely available: (https://agage2.eas.gatech.edu/data_archive/agage/)

There you should find a tar.gz file containing netcdf files, you can extract it and set 
the `netcdf_directory` parameter from the `run_config.json` file to the extracted folder.

## Running the app

The main file is `app.py` which is a Dash app. To run the app, you need to have the following packages installed:

```bash
python -m gcviz.app
```

This will run your app on the localhost. You should be able to see a 
link in the terminal where you can access the app.

If you want to run your app on a local webserver, 
this is currently not supported.

## Configuration

The configuration file is `run_config.json`. You can set the following parameters:
All parameters are optional having default values, except for the `netcdf_directory` parameter. 

- `netcdf_directory`: the directory where the netcdf files are stored
- `logging`: various parameters for logging
    - `level`: the logging level. Can be `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- `network`: parameters for the network
    - `host`: the host (ip) of the network
    - `port`: the port of the network
- `data`: parameters related to the data
    - `invalid_values`: a value for the missing data

Other parameters can be given in case some views require them.


If you want to run the app with a different config file, you can specify the path to the config file as an argument:

```bash
python app.py --config path/to/config.json
```

## Implementing new views

To implement a new view, you should start by looking at the implemented views 
in the `gcviz/views` folder. You can create a new file in this folder and 
implement your view in a similar way.

The following applies to all views:
* The view should be a instance of the `View` class.
* You can create call backs that update your view. Look at existing callbacks for examples.
* Your view can be added to gcviz by adding it in the `run_config.json` file.

Gcviz makes use of `dash` and `plotly` for the visualizations. You don't need to be 
an expert in these libraries to implement a new view.
Following this tutorial should be enough:
https://dash.plotly.com/tutorial




## Contributing & Support

We are happy of any contributions. Please raise an issue or create a merge request.

## Authors and acknowledgment
Thanks to all the contributors to this project.

See the list in the `pyproject.toml` file.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
