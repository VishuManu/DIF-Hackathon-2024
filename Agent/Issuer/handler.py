
import json
import base64
from enum import Enum
from uuid import uuid4
from flask import Flask, render_template, request, jsonify
import sys
sys.path.append("../")

app = Flask(__name__)

CONNECTONS_DATA = []


from CONST.CONST import *
from CONST.GOAL_C import *
from Wallet_Helper.main import Helper

class Initial_Invitation_Sending_Medium(Enum):
    QR = 0
    URL = 1
    BLUETOOTH = 2


class Issuer_Handler:
    
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.my_init_did = "did:key:zxcvvbwswewewqe123456789"
        self.mode = Initial_Invitation_Sending_Medium.QR
        self.helper = Helper(local_host="http://127.0.0.1:3000/")
        self.recipientKeys = ""
        self.label = ""

    def __setup_listener_routes__(self):

        @self.app.route(CREATE_INVITATION, methods=['GET'])
        def __create_invitation__():
            _data_template = {
                "type": "https://didcomm.org/out-of-band/2.0/invitation",
                "id": str(uuid4()),
                "from": self.my_init_did,
                "body": {
                    "goal_code": GOAL_INVITATION,
                    "goal": "Message Sent To Establish Peer to Peer Connection",
                    "label": self.label,
                    "accept": ["didcomm/v2"],
                },
                "attachments": [
                    {
                        "id": "request-0",
                        "media_type": "application/json",
                        "data": {
                            "json": {
                                "type": "https://didcomm.org/didexchange/1.0/request",
                                "id": "abcd1234",
                                "label": self.label,
                                "from": self.my_init_did,
                                "service": [
                                    {
                                        "id": "did:example:alice#service-1",
                                        "type": "DIDCommMessaging",
                                        "serviceEndpoint": HOST + RECEIVE_INVITATION,
                                        "recipientKeys": [
                                            self.recipientKeys
                                        ],
                                        "routingKeys": []
                                    }
                                ]
                            }
                        }
                    }
                ]
            }

            result = None
            if self.mode == Initial_Invitation_Sending_Medium.QR:
                encoded = base64.urlsafe_b64encode(
                    str(_data_template).encode('utf-8'))
                result = f"{HOST}/invite_url?_oob={encoded.decode('utf-8')}"

            return result

        @self.app.route("/invite_url", methods=['GET'])
        def __invite_url__():
            obb = request.args.get("_oob")
            try:
                _json = base64.urlsafe_b64decode(obb.encode('utf-8'))
                print(_json.decode('utf-8'))
            except Exception as EE:
                print(EE)
            
            return "Ok"
        


    


        @self.app.route(RECEIVE_INVITATION,methods=['POST'])
        def __receive_invitation__():
            _json = request.get_json()
            _to = _json['to']
            if _to:
                # Calling Request to wallet to check did key present or not
                pass
            print(_json)
            _body = _json['body']
            if _body:
                if _body['goal_code'] != PEER_EXCHANGE_AND_ACCEPT_INVITATION:
                    raise Exception("goal code is malformed")

                _from = _json['from']
                if _from:
                    _did_granuals = _from.split(":")
                    if len(_did_granuals) == 3 and _did_granuals[0] == "did" and _did_granuals[1] == "peer":
                        _encoded = _did_granuals[-1]
                            # save peer did to wallet            
            
            return "Done"

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    isuer = Issuer_Handler()
    isuer.__setup_listener_routes__()
    isuer.run()
