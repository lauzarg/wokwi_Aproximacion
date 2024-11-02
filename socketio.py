import usocket as socket
import ustruct as struct
import ubinascii
import ujson
import time

class Client:
    def __init__(self):
        self.s = None
        self.connected = False
        self.events = {}

    def connect(self, url):
        self.s = socket.socket()
        ai = socket.getaddrinfo(url, 80)
        addr = ai[0][-1]
        self.s.connect(addr)
        self.s.send(b'GET /socket.io/?EIO=3&transport=websocket HTTP/1.1\r\n')
        self.s.send(b'Host: %s\r\n' % url)
        self.s.send(b'Upgrade: websocket\r\n')
        self.s.send(b'Connection: Upgrade\r\n')
        self.s.send(b'Sec-WebSocket-Key: %s\r\n' % ubinascii.b2a_base64(struct.pack('!Q', int(time.time() * 1000))))
        self.s.send(b'Sec-WebSocket-Version: 13\r\n\r\n')
        self.s.recv(1024)
        self.connected = True
        self._emit('connect')

    def on(self, event, callback):
        self.events[event] = callback

    def _emit(self, event, *args):
        if event in self.events:
            self.events[event](*args)

    def emit(self, event, data):
        if self.connected:
            message = ujson.dumps({'event': event, 'data': data})
            self.s.send(b'\x81' + struct.pack('!H', len(message)) + message)

    def wait(self):
        while self.connected:
            data = self.s.recv(1024)
            if data:
                self._handle_message(data)

    def _handle_message(self, data):
        if data[0] == 129:
            length = data[1] & 127
            if length == 126:
                length = struct.unpack('!H', data[2:4])[0]
                message = data[4:4+length]
            else:
                message = data[2:2+length]
            message = ujson.loads(message)
            self._emit(message['event'], message['data'])

    def close(self):
        self.connected = False
        self.s.close()