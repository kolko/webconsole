# -*- coding: utf-8 -*-
from twisted.python import log
from twisted.internet import reactor
from twisted.web import server, resource

import settings
from subscriber import Subscriber


class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        # if request.path == '/json_data2':
        with open('test_client.html', 'r') as f:
            html = f.read()
        uid = make_process()
        socket_ip = settings.LOCAL_IP
        socket_port = settings.WEB_SOCKET_PORT
        html = html.replace('$$$PROCESS_KEY$$$', uid)\
            .replace('$$$SOCKET_IP$$$', socket_ip)\
            .replace('$$$SOCKET_PORT$$$', str(socket_port))
        return html


def make_process():
    uid = Subscriber().spawn_process()
    return uid


def run():
    site = server.Site(Simple())
    reactor.listenTCP(settings.WEB_HTTP_PORT, site)