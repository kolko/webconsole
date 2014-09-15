# -*- coding: utf-8 -*-
import sys

from twisted.python import log
from twisted.internet import reactor

import web_server
import websocket_server
from config_loader import ConfigLoader


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    websocket_server.run()
    web_server.run()

    cf_l = ConfigLoader()

    reactor.run()