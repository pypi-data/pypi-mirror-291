import json

# Default configurations
DEFAULT_CONFIG = {
    "output_types": {
        "string": "\n".join,
        "list": lambda x: "\n".join(x),
        "dict": lambda x: json.dumps({"data": x}, indent=4)
    },
    "save": True
}

def get_config():
    """Return the configuration settings."""
    return DEFAULT_CONFIG
