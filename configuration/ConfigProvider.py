import configparser

global_config = configparser.ConfigParser(interpolation=None)
global_config.read('test_config.ini')

class ConfigProvider:
    def __init__(self) -> None:
        self.config = global_config

    def get(self, section: str, prop: str, fallback=None):
        return self.config.get(section, prop, fallback=fallback)

    def getint(self, section: str, prop: str, fallback=0):
        try:
            return self.config.getint(section, prop, fallback=fallback)
        except ValueError:
            return fallback

    def get_ui_url(self, fallback=""):
        return self.get("ui", "base_url", fallback)