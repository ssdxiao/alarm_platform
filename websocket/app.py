from websocket import WebSocketServer
from websocket import WebSocketRequestHandler



web = WebSocketServer(WebSocketRequestHandler, listen_host="0.0.0.0", listen_port=8088, verbose=True)
web.start_server()



