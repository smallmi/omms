import logging
import socket
from controller.dwebsocket import factory
from .websocket import DefaultWebSocket
from .protocols import get_websocket_protocol


logger = logging.getLogger(__name__)


class SocketWarp(object):

    def __init__(self, request):
        self.request = request
        self.closed = False


class WebSocketFactory(factory.WebSocketFactory): 

    def get_wsgi_sock(self):
        if 'gunicorn.socket' in self.request.META:
            sock = self.request.META['gunicorn.socket']
        else:
            # print('获取wsgi.input')
            # print(self.request.META['wsgi.input'])
            wsgi_input = self.request.META['wsgi.input']
            if hasattr(wsgi_input, '_sock'):
                sock = wsgi_input._sock
            elif hasattr(wsgi_input, 'rfile'):  # gevent
                if hasattr(wsgi_input.rfile, '_sock'):
                    sock = wsgi_input.rfile._sock
                else:
                    sock = wsgi_input.rfile.raw._sock  
            elif hasattr(wsgi_input, 'raw'):
                sock = wsgi_input.raw._sock
            else:
                sock = wsgi_input.stream
                # print('Socket not found in wsgi.input')
                # raise ValueError('Socket not found in wsgi.input')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        return sock

    def create_websocket(self):
        if not self.is_websocket():
            return None
        try:
            # print('进入create_websocket')
            # print(self.get_wsgi_sock())

            protocol = get_websocket_protocol(self.get_websocket_version())(
                sock = self.get_wsgi_sock(),
                headers = self.request.META
            )
            # print('获取websocket协议' + str(protocol))
            return DefaultWebSocket(protocol=protocol)
        except KeyError as e:
            # print('获取websocket协议失败')
            logger.exception(e)
        return None
