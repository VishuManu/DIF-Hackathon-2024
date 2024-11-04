import sys
import datetime

sys.path.append("../")
from CONST.GOAL_C import *
from CONST.CONST import *
from CONST.TYPE import *
import typing
from uuid import uuid4


class Template:
    def __invitation_response__(
        self, label: typing.Optional[str], _from: str, to: str, parent_id: str
    ):
        INVITATION_REPONSE = {
            "id": str(uuid4()),
            "pthid": parent_id,
            "type": "https://didcomm.org/out-of-band/2.0/handshake-reply",
            "from": _from,
            "to": to,
            "body": {
                "label": label,
                "goal_code": PEER_EXCHANGE_AND_ACCEPT_INVITATION,
                "goal": "Accept the connection and proceed to DID exchange",
            },
        }

        return INVITATION_REPONSE

    def __trust_ping__(self, _from: str):
        _payload = {
            "type": PING_URL,
            "id": str(uuid4()),
            "from": _from,
            "body": {"response_requested": True},
        }
        return _payload

    def __presentation_msg__(self, data):
        _data_template = {
            "type": "https://didcomm.org/out-of-band/2.0/invitation",
            "id": str(uuid4()),
            "from": data["from"],
            "to": data["to"],
            "body": {
                "goal_code": ASK_PRESENTATION,
                "goal": "Message To Ask For Presentation",
                "accept": ["didcomm/v2", "didcomm/aip2;env=rfc587"],
            },
            "attachments": [
                {
                    "id": str(uuid4()),
                    "media_type": "application/json",
                    "data": {"json": data["payload"]},
                }
            ],
        }
        return _data_template

    def zkp_request(self, data):
        _data_template = {
            "type": "https://didcomm.org/out-of-band/2.0/zkp_request",
            "id": str(uuid4()),
            "from": data["from"],
            "to": data["to"],
            "body": {
                "goal_code": ASK_ZKP,
                "goal": "Message To Ask For Presentation",
                "accept": ["didcomm/v2", "didcomm/aip2;env=rfc587"],
            },
            "attachments": [
                {
                    "id": str(uuid4()),
                    "media_type": "application/json",
                    "data": {"json": {"cred_id": data["cred_id"]}},
                }
            ],
        }
        return _data_template

    def __create_invitation__(self, label: str, init_did: str, agent_URL: str):
        _data_template = {
            "type": "https://didcomm.org/out-of-band/2.0/invitation",
            "id": str(uuid4()),
            "from": init_did,
            "body": {
                "goal_code": GOAL_INVITATION,
                "goal": "Message Sent To Establish Peer to Peer Connection",
                "label": label,
                "accept": ["didcomm/v2", "didcomm/aip2;env=rfc587"],
            },
            "attachments": [
                {
                    "id": str(uuid4()),
                    "media_type": "application/json",
                    "data": {
                        "json": {
                            "type": "https://didcomm.org/didexchange/1.0/request",
                            "id": str(uuid4()),
                            "label": label,
                            "from": init_did,
                            "service": [
                                {
                                    "id": "did:example:alice#service-1",
                                    "type": "DIDCommMessaging",
                                    "serviceEndpoint": agent_URL + RECEIVE_INVITATION,
                                    "recipientKeys": [],
                                    "routingKeys": [],
                                }
                            ],
                        }
                    },
                }
            ],
        }
        return _data_template

    def __didcomm_encrypted_msg__(self):
        pass
