import os
import re

import click
import tomli

DEFAULT_CONFIG_FILES = [
    os.path.join(os.getcwd(), "pyproject.toml"),
]


class CommandConfig:
    """
    The base configuration for a command group configuration.
    """

    pass


class Config:
    """
    The base configuration for the vitaleey CLI configuration in pyproject.toml.

    NOTE: To retrieve the data call `.load()` on the instance.
    """

    dataclass: CommandConfig | None = None

    def __init__(self, main_section: str = "vitaleey"):
        self.main_section = main_section

        self._validate_classname()

    def __call__(self, *args, **kwargs):
        return self.load(*args, **kwargs)

    def get_dataclass(self):
        return self.dataclass

    def _convert_classname(self):
        """
        Get the command group configuration
        """

        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()

    def _validate_classname(self):
        if not self._convert_classname().endswith("_config"):
            raise click.ClickException("The class name must end with _config")

    def _filter_command_group(self, config):
        """
        Filter the command group from the configuration
        """

        command_group = self._convert_classname().replace("_config", "")
        return config.get(command_group, {})

    def _parse_dataclass(self, config):
        """
        Parse config to dataclass
        """

        dataclass = self.get_dataclass()
        if dataclass is not None and config:
            return dataclass(**config)
        return config

    def load(self):
        """
        Load the configuration from the pyproject.toml file
        """
        config = {}
        for path in DEFAULT_CONFIG_FILES:
            if os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        config = tomli.load(f)
                except tomli.TOMLDecodeError as e:
                    click.ClickException(f"Could not load pyproject.toml file: {e}")
                    config = {}
        config = config.get("tool", {}).get(self.main_section, {})
        if not config:
            raise click.ClickException("Could not load the vitaleey configuration")

        config = self._filter_command_group(config)

        return self._parse_dataclass(config)


class PoetryConfig(Config):
    """
    Poetry configuration

    Here you can find all the basic project configuration.
    """

    def __init__(self):
        super().__init__("poetry")

    def _change_value(self, path, section, key, value):
        """
        Update the lines
        """

        lines = []
        at_section = False
        at_end_of_section = False
        for line in open(path, "r"):
            if line.startswith(section):
                at_section = True

            if at_section and not at_end_of_section:
                if line.startswith(key):
                    line = f'{key} = "{value}"\n'

            if at_section and line.startswith("\n"):
                at_end_of_section = True

            lines.append(line)
        return ("").join(lines)

    def _update_configuraion(self, path, data):
        """
        Update the configuration in the pyproject.toml file
        """

        with open(path, "w") as f:
            f.write(data)

    def set(self, key: str, value: str):
        """
        Set value in the configuration
        """

        for path in DEFAULT_CONFIG_FILES:
            if os.path.exists(path):
                data = self._change_value(path, "[tool.poetry]", key, value)
                self._update_configuraion(path, data)
                break  # Only update the first file


class EnvironmentNames(object):
    DEVELOPMENT = ["dev", "development"]
    ACCEPTANCE = ["acc", "acceptance"]
    PRODUCTION = ["prd", "prod", "production"]

    def groups(self):
        return {
            "development": self.DEVELOPMENT,
            "acceptance": self.ACCEPTANCE,
            "production": self.PRODUCTION,
        }

    def get_group(self, name):
        for group, names in self.groups().items():
            if name in names:
                return group

    def get_group_options(self, name):
        """
        Get the group options for a given environment name.
        The option name will be used to select the environment.

        Group: development
            Options: ['dev', 'development']

        Group: acceptance
            Options: ['acc', 'acceptance']

        Group: production
            Options: ['prd', 'prod', 'production']
        """

        for group, names in self.groups().items():
            if name in names:
                return names

    def names(self):
        names = []
        for group in self.groups().values():
            names.extend(group)
        return names


environment_names = EnvironmentNames()

ENVIRONMENTS = environment_names.names()

poetry_config = PoetryConfig()
