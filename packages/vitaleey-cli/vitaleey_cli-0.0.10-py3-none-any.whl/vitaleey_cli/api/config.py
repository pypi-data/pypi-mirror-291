from dataclasses import dataclass, field

import click

from vitaleey_cli.config import Config

__all__ = ["api_gateway_config"]


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


ENVIRONMENTS = EnvironmentNames().names()


@dataclass(frozen=True)
class ApiGatewayDataclass:
    """
    Configuration for an APIGateway environment:
        development, acceptance, production

    Options:
    - endpoint_dir: The directory where the endpoint files are stored
    ```
    """

    endpoint_dir: str = "config"


@dataclass(frozen=True)
class EnvironmentDataclass:
    """
    Configuration for all the environments:

    Options:
    - environments: The environments for the APIGateway
    """

    environments: dict[str, ApiGatewayDataclass] = field(default_factory=dict)


class ApiGatewayConfig(Config):
    """
    API Gateway configuration
    """

    def _load_env_configs(self, config):
        """
        Load the environments configurations
        """

        # Get environments
        environments = {}

        config_envs: dict[str, dict] = config.get("env", {})

        # Retrieve environment configurations
        for group, group_config in config_envs.items():
            kwargs = {
                key: value
                for key, value in group_config.items()
                if key in ApiGatewayDataclass.__annotations__
            }

            # Fill missing keys with global_config
            for key in ApiGatewayDataclass.__annotations__:
                if not kwargs.get(key) and config.get(key):
                    kwargs[key] = config.get(key)
            environments[group] = ApiGatewayDataclass(**kwargs)
        return EnvironmentDataclass(environments=environments)

    def load(self, environment: str):
        """
        Load the configuration based on the environment
        """

        if environment not in ENVIRONMENTS:
            raise click.UsageError(f"Invalid environment, choose from: {ENVIRONMENTS}")

        click.secho(
            f"Loading configuration for {EnvironmentNames().get_group(environment)} environment",
            bold=True,
        )

        config = super().load()
        env_configs = self._load_env_configs(config)

        environment_options = EnvironmentNames().get_group_options(environment)

        for env in environment_options:
            env_config = env_configs.environments.get(env)
            if env_config:
                return env_config


api_gateway_config = ApiGatewayConfig()
