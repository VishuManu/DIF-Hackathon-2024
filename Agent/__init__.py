'''import logging
from websocket_server import WebsocketServer
import time

def __new_msg__(client,server,message):
    if message:
        print(message)
    pass

def __client_disconnect__(client,server):
    print(client)
    time.sleep(5)
    print(server.clients)

def __client_connect__(client,server):
    pass

server = WebsocketServer(host='127.0.0.1',port=6969,loglevel=logging.INFO)
server.set_fn_message_received(__new_msg__)
server.set_fn_client_left(__client_disconnect__)
server.set_fn_new_client(__client_connect__)
server.run_forever()

'''


from Prover_Holder.handler import Holder


class Agent:
    def __init__(self,port,type:str):
        self.port = port
        if type == "Holder":
            self.holder_prover = Holder()
        else:
            self

