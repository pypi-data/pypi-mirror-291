import os
import configparser

from ZRunAuto.config.path import CONFIG_PATH


class Config(object):
    def __init__(self, ):
        self._path = CONFIG_PATH
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini" + self._path)
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')

    def get(self, section, name):
        return self._config.get(section, name)

    def getRaw(self, section, name):
        return self._configRaw.get(section, name)


global_config = Config()
