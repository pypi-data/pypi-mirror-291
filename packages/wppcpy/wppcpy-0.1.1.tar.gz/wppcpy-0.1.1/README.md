# WPPCPY - Wordpress Plugin Checker

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/shahmal1yev/wppcpy?label=latest&style=flat)
![GitHub last commit](https://img.shields.io/github/last-commit/shahmal1yev/wppcpy)
![GitHub stars](https://img.shields.io/github/stars/shahmal1yev/wppcpy)
![GitHub issues](https://img.shields.io/github/issues/shahmal1yev/wppcpy)

```wppcpy``` is a Python package designed to verify if a directory meets the necessary constraints to be considered a
valid WordPress plugin. It checks for essential headers in the main PHP file and ensures the presence of required files
like `readme.txt`.

## Features

- **Header Validation**: Checks for the existence of key headers in the main PHP file, such as `Plugin Name`,
  `Plugin URI`, `Description`, `Version`, and more.
- **File Validation**: Ensures that required files like `readme.txt` are present in the plugin directory.

## Installation

You can install the ```wppcpy``` using pip:

```bash
pip install wppcpy
```

## Usage

Here's a basic example of how to use the Plugin Validator:

```python
import wppcpy.constraints

if __name__ == "__main__":
    plugin_path = "/var/www/wordpress/vns/booknetic.run/wp-content/plugins/booknetic"

    main_file_name = 'init.php'

    constraints = [
        constraints.header.PluginName(plugin_path, main_file_name),
        constraints.header.Description(plugin_path, main_file_name),
        constraints.header.Version(plugin_path, main_file_name),
        constraints.file.MainFile(plugin_path, main_file_name),
    ]

    all_valid = all(constraint.validate() for constraint in constraints)

    if all_valid:
        print("Directory is a wordpress plugin by constraints.")
    else:
        print("Directory is not a wordpress plugin by constraints.")
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find a bug or have a
suggestion.