"""A class or function to parse the config file and return the values as a dictionary.

The config file itself can be any of the following formats:

- ryo: means 'roll your own' and is a simple text file with key-value pairs separated by an equals sign. For example:
```
location = "Moondalup City Square Parking"
number_of_spaces = 192
```
**you** read the file and parse it into a dictionary.
- json: a json file with key-value pairs. For example:
```json
{location: "Moondalup City Square Parking", number_of_spaces: 192}
```
json is built in to python, so you can use the json module to parse it into a dictionary.
- toml: a toml file with key-value pairs. For example:
```toml
[location]
name = "Moondalup City Square Parking"
spaces = 192
```
toml is part of the standard library in python 3.11, otherwise you need to install tomli to parse it into a dictionary.
```bash
python -m pip install tomli
```
see [realpython.com](https://realpython.com/python-toml/) for more info.

Finally, you can use `yaml` if you prefer.



"""
import os
import toml

import smartpark


def parse_config(config_filepath) -> dict:
    """Parse the config file and return the values as a dictionary"""
    with open(config_filepath, "r") as file:
        config = toml.load(file)

    config = config['config']

    common_config = {k: v for k, v in config.items() if k in ["broker", "port", "topic-root"]}

    sensor_config = common_config | config["sensor"]
    carpark_config = common_config | config["carpark"]
    display_config = common_config | config["display"]

    return {"sensor": sensor_config, "carpark": carpark_config, "display": display_config}

def _get_config_path():
    current_dir = os.path.dirname(os.path.abspath(smartpark.__file__))
    config_file_path = os.path.join(current_dir, r'config\config.toml')
    return config_file_path

CONFIG_PATH = _get_config_path()


if __name__ == "__main__":
    print(parse_config(CONFIG_PATH)['sensor'])
    print(parse_config(CONFIG_PATH)['carpark'])
    print(parse_config(CONFIG_PATH)['display'])
