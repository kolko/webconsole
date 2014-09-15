# -*- coding: utf-8 -*-
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

import settings
from subscriber import Subscriber, UidNotExists


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        uid = request.params.get('uid')
        if not uid:
            self.close()
        uid = uid[0]
        self.subscriber = Subscriber()
        try:
            self.subscriber.websocket_attach(self, uid)
        except UidNotExists:
            self.close()
        self.uid = uid
        log.msg("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        log.msg("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            log.msg("Binary message received: {0} bytes".format(len(payload)))
        else:
            log.msg("Text message received: {0}".format(payload.decode('utf8')))
        self.subscriber.websocket_data(self, self.uid, payload)

    def onClose(self, wasClean, code, reason):
        if self.uid:
            try:
                self.subscriber.websocket_deattach(self, self.uid)
            except Exception, e:
                log.err(e)
        log.msg("WebSocket connection closed: {0}".format(reason))


def run():
    ip = settings.LOCAL_IP
    port = settings.WEB_SOCKET_PORT
    factory = WebSocketServerFactory("ws://{0}:{1}".format(ip, port), debug=False)
    factory.protocol = MyServerProtocol
    reactor.listenTCP(port, factory)