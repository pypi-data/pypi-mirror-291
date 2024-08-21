"""Main entry point for the gcviz package."""

import argparse
import json
from pathlib import Path

from gcviz.app import create_app

parser = argparse.ArgumentParser(description="gcviz")

# Make it the first argument
parser.add_argument(
    "--config",
    type=str,
    default="run_config.json",
    help="The path to the config file",
)

args = parser.parse_args()

# Read the config
config_path = Path(args.config)
if not config_path.exists():
    raise FileNotFoundError(
        f"Config file not found: {config_path}. Please provide a valid path."
    )


with open(config_path) as f:
    config = json.load(f)

assert isinstance(config, dict)


app = create_app(config)


app.run(
    debug=True,
    host=config.get("newtork", {}).get("host", "127.0.0.1"),
    port=config.get("newtork", {}).get("port", 8050),
)
