# -*- coding: utf-8 -*-
import random
from collections import namedtuple

from twisted.python import log
from twisted.internet import reactor

from process_protocol import Process


class UidNotExists(Exception):
    pass


UidItem = namedtuple('UidItem', ['process', 'subscribers'])


class Subscriber(object):
    """Create process, handle events"""
    _instance = None
    def __new__(cls, *args, **kwargs):
        #Singleton
        if not cls._instance:
            cls._instance = super(Subscriber, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not getattr(self, 'uid_list', None):
            self.uid_list = {}

    def spawn_process(self):
        uid = '%s' % random.randrange(99*99*99*99*99*99*99)
        process = Process(self, uid)
        self.uid_list[uid] = UidItem(process, [])
        reactor.spawnProcess(process, 'bash', ["bash", ], env=None)
        return uid

    def process_alert_data(self, uid, data):
        """Alert all subscribers"""
        uid_item = self._get_uid_item(uid)
        for subscriber in uid_item.subscribers:
            subscriber.sendMessage(data)

    def process_alert_close(self, uid, exit_code):
        """Alert all subscribers"""
        uid_item = self._get_uid_item(uid)
        for subscriber in uid_item.subscribers:
            subscriber.close()

    def _get_uid_item(self, uid):
        if uid not in self.uid_list:
            raise UidNotExists()
        return self.uid_list[uid]

    def websocket_attach(self, socket, uid):
        uid_item = self._get_uid_item(uid)
        uid_item.subscribers.append(socket)
        socket.sendMessage(uid_item.process.get_all_data())

    def websocket_deattach(self, socket, uid):
        uid_item = self._get_uid_item(uid)
        uid_item.subscribers.remove(socket)

    def websocket_data(self, socket, uid, data):
        uid_item = self._get_uid_item(uid)
        uid_item.process.transport.write(data)