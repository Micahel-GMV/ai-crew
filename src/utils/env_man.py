import configparser
import os

class EnvMan:
    _config = None  # This will store the singleton instance of the configuration

    @classmethod
    def get_config(cls):
        if cls._config is None:
            root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(root_path, 'config.ini')
            config = configparser.ConfigParser()
            config.read(config_path)
            cls._config = config
        return cls._config

config = EnvMan().get_config()

