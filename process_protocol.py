# -*- coding: utf-8 -*-
from twisted.internet import protocol


class Process(protocol.ProcessProtocol):
    def __init__(self, subscriber, uid):
        self.subscriber = subscriber
        self.uid = uid
        self.handlers = []
        self.data = ""

    #protocol

    def connectionMade(self):
        print "MyPP connectionMade!"

    def outReceived(self, data):
        print "MyPP outReceived! with %d bytes!" % len(data)
        self.data = self.data + data
        self.handlers_alert(data)

    def errReceived(self, data):
        print "MyPP errReceived! with %d bytes!" % len(data)
        self.data = self.data + data
        self.handlers_alert(data)

    def inConnectionLost(self):
        print "MyPP inConnectionLost! stdin is closed! (we probably did it)"

    def outConnectionLost(self):
        print "MyPP outConnectionLost! The child closed their stdout!"

    def errConnectionLost(self):
        print "MyPP errConnectionLost! The child closed their stderr."

    def processExited(self, reason):
        print "MyPP processExited, status %s" % (reason.value.exitCode,)

    def processEnded(self, reason):
        print "MyPP processEnded, status %s" % (reason.value.exitCode,)
        print "MyPP quitting"

    #end protocol
    def handlers_alert(self, data):
        self.subscriber.process_alert_data(self.uid, data)

    def get_all_data(self):
        return self.data