# -*- coding: utf-8 -*-
import os
from ConfigParser import ConfigParser

import settings


class ConfigLoader(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        #Singleton
        if not cls._instance:
            cls._instance = super(ConfigLoader, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not getattr(self, 'scripts', None):
            self.reload_config()

    def reload_config(self):
        self.scripts = {}
        cf_parser = ConfigParser()
        scripst_path = settings.SCRIPTS_PATH
        files = [f for f in os.listdir(scripst_path) if f.endswith('.ini')]
        for file in files:
            cf_parser.read(file)
            print(1)