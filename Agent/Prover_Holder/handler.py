import json
import base64
from enum import Enum
from uuid import uuid4
from flask import Flask, render_template, request, Response, jsonify
import sys
from datetime import datetime
from tinydb import TinyDB,Query

sys.path.append("../")
from CONST.GOAL_C import *
from CONST.TYPE import TYPE_INVITATION_URL
import os
import re
import tinydb
from CONST.CONST import *
from CONST.TYPE import *

app = Flask(__name__)
import requests
from flask_cors import CORS

# from Test.did_generate import generate
from urllib.parse import urlparse, parse_qs
import urllib
from did.peer import Peer_DID
from Utils.didcommv2_message_templates import *
from typing import Optional, Sequence, Literal
from dataclasses import dataclass, field

CONNECTONS_DATA = []
RELATIONSHIPS = (
    "authentication",
    "assertionMethod",
    "keyAgreement",
    "capabilityDelegation",
    "capabilityInvocation",
)

Relationship = Literal[
    "authentication",
    "assertionMethod",
    "keyAgreement",
    "capabilityDelegation",
    "capabilityInvocation",
]


@dataclass
class Multikey:
    """Multikey specification."""

    type: str = field(init=False, default="Multikey")
    context: str = field(init=False, default="https://w3id.org/security/multikey/v1")

    multikey: str
    relationships: Optional[Sequence[Relationship]] = None
    ident: Optional[str] = None


class Initial_Invitation_Sending_Medium(Enum):
    QR = 0
    URL = 1
    BLUETOOTH = 2


class Holder:
    def __init__(self, port) -> None:
        self.app = Flask(__name__)
        CORS(self.app)
        self.my_init_did = "did:test"
        # self.db = DB()
        self.template = Template()
        self.mode = Initial_Invitation_Sending_Medium.QR
        self.recipientKeys = ""
        self.port = port
        self.my_peer = ""
        self.did_key = ""
        self.label = ""

    def __setup_init_connection_routes__(self):
        @self.app.route(RECEIVE_PEER_EXCHANGE_RESPONSE, methods=["POST"])
        def __send_accept_response__():
            # STEP 4
            _decoded = json.loads(request.json["data"])
            if _decoded:
                if _decoded["type"] == HANDSHAKE_REPLY:
                    # TODO Check if that key is contain in our  wallet
                    if _decoded["to"]:
                        _body = _decoded["body"]
                        if (
                            _body
                            and _body["goal_code"]
                            == PEER_EXCHANGE_AND_ACCEPT_INVITATION
                        ):
                            _received_peer = _decoded["from"]
                            _pr = Peer_DID(_received_peer)
                            _received_peer = _pr.__validate__()
                            from did_peer_4 import decode

                            _decoded_peer = decode(_received_peer)
                            if _received_peer is None:
                                return

                            qr = tinydb.Query()
                            tn = tinydb.TinyDB("../../src/Wallet/db.json")

                            _data = tn.search(qr.pub_key == self.did_key)
                            _peers = _data[0]["peers"]
                            for _p in _peers:
                                if _p["connection_id"] == request.json["ycid"]:
                                    _p["their_connection_id"] = request.json["mycid"]
                                    _p["their_did"] = _received_peer

                            tn.update({"peers": _peers}, qr.pub_key == self.did_key)

                            # TODO decoding peer did fetching URLs of endpoint
                            server_uri = (
                                _decoded_peer["service"][0]["serviceEndpoint"]["uri"]
                                if _decoded_peer["service"]
                                else None
                            )
                            server_uri = server_uri + PING
                            if server_uri:
                                _ping = self.template.__trust_ping__(self.my_peer)
                                _ = requests.post(server_uri, json=json.dumps(_ping))
                                print("Ping sent ....")
                            return "Yo"
                            # TODO SAVE Peer to wallet with connection

                        else:
                            return Response(
                                "Body & Body Code is not valid",
                                500,
                                mimetype="text/plain",
                            )
                    else:
                        return Response(
                            "Reeiver Not Define", 500, mimetype="text/plain"
                        )
            else:
                return Response("Decoded Data is curropted", 500, mimetype="text/plain")

        @self.app.route("/accept", methods=["POST"])
        def __accept_init_invite__():
            # STEP 2 Accept Inviation
            _URL = request.json
            my_key_did = _URL["my_key"]
            self.did_key = my_key_did
            _URL = urlparse(_URL["url"])
            query_params = parse_qs(_URL.query)
            _OBB = query_params["_oob"][0]
            _TYPE = query_params["type"][0]

            try:
                _json = base64.urlsafe_b64decode(_OBB.encode("utf-8"))
                _json = _json.decode("utf-8").replace("'", '"')
                _json = json.loads(_json)
            except (ValueError, json.JSONDecodeError) as e:
                raise ValueError(f"Failed to decode or parse the JSON: {e}")

            if isinstance(_json, dict) and all(
                key in _json for key in ["type", "id", "from", "body", "attachments"]
            ):
                if _json["type"] == TYPE_INVITATION_URL:
                    _pid = _json.get("id")
                    _from = _json.get("from")
                    _body = _json.get("body")
                    if (
                        isinstance(_body, dict)
                        and "goal_code" in _body
                        and "accept" in _body
                    ):
                        if _body.get("goal_code") == GOAL_INVITATION:
                            _label = _body.get("label", "")
                            _accept_protocol = _body.get("accept")[0]
                            _attachments = _json.get("attachments", [])
                            if len(_attachments) > 0:
                                _attachment = _attachments[0]
                                if _attachment.get("media_type") == MEDIA_TYPE_JSON:
                                    _data = _attachment.get("data", {}).get("json", {})
                                    if "from" in _data and "service" in _data:
                                        _from = _data.get("from")
                                        _service = _data.get("service")[0]
                                        _endpoint = _service.get("serviceEndpoint", "")
                                        _parsed_endpoint = urllib.parse.urlparse(
                                            _endpoint
                                        )
                                        if (
                                            _parsed_endpoint.hostname
                                            and _parsed_endpoint.path
                                            and _parsed_endpoint.path
                                            == RECEIVE_INVITATION
                                        ):
                                            _host = _parsed_endpoint.hostname
                                            _path = _parsed_endpoint.path

                                            template = Template()
                                            # TODO : Generating Peer DID from  & Encoding the data with my signature and there did:key

                                            from Peer.did_generate import generate

                                            _peer_created = generate()

                                            self.my_peer = _peer_created
                                            _date = datetime.datetime.now()
                                            qr = tinydb.Query()
                                            tn = tinydb.TinyDB(
                                                "../../src/Wallet/db.json"
                                            )

                                            _data = tn.search(qr.pub_key == my_key_did)
                                            _unq = str(uuid4())
                                            _data[0]["peers"].append(
                                                {
                                                    "connection_id": _unq,
                                                    "my_did": _peer_created,
                                                    "their_did": "",
                                                    "their_connection_id": "",
                                                    "status": "peer_sent",
                                                    "createdAt": str(_date),
                                                }
                                            )

                                            tn.update(
                                                _data[0], qr.pub_key == my_key_did
                                            )

                                            _json_test = (
                                                template.__invitation_response__(
                                                    "Me", _peer_created, _from, "test"
                                                )
                                            )
                                            _client = requests.post(
                                                "http://127.0.0.1:5000"
                                                + RECEIVE_INVITATION
                                                + "/"
                                                + _TYPE,
                                                json={
                                                    "conid": _unq,
                                                    "data": json.dumps(_json_test),
                                                },
                                            )
                                            if _client.status_code == 200:
                                                return "Response Sent With My Peer DID to issuer"
                                            else:
                                                return f"Err with Status Code {_client.status_code}"

                                        else:
                                            raise ValueError(
                                                "Invalid service endpoint URL."
                                            )
            else:
                raise ValueError("Invalid or missing required JSON fields.")

        @self.app.route("/get_credential", methods=["POST"])
        def __get_from_constrains__():
            _fields = request.json
            constrains = []
            credentials = []
            for x in _fields["fields"]:
                paths = x["path"]
                for p in paths:
                    p = p.replace("$", "")
                    filter_data = x.get("filter", {})

                    constrains.append(
                        {
                            "location": p,
                            "type": filter_data.get("type", ""),
                            "opr": list(filter_data.keys())[-1]
                            if filter_data
                            and isinstance(
                                filter_data.get(list(filter_data.keys())[-1]), dict
                            )
                            else "",
                            "pattern": filter_data.get(list(filter_data.keys())[-1], "")
                            if filter_data
                            else "",
                        }
                    )
            qr = tinydb.Query()
            tn = tinydb.TinyDB("../../src/Wallet/db.json")
            _all = tn.all()[0]
            creds = _all["creds"]
            result = []
            cred_id = []
            for x in constrains:
                _where = x["location"].split(".")
                root = _where[1]
                sub = _where[2] if len(_where) > 2 else None
                # Handling "contains" operation
                if x.get("opr") == "contains":
                    qr = x.get("pattern")
                    if isinstance(qr, dict):
                        _data = qr["pattern"]
                        for w in creds:
                            w = w["w3c"]
                            if sub:
                                if _data in w.get(root, {}).get(sub, ""):
                                    print("Hello")
                                    cred_id.append(w["id"])
                            else:
                                print(w.get(root, ""))
                                if _data in w.get(root, ""):
                                    print("Hello")
                                    cred_id.append(w["id"])

                elif not x.get("opr"):
                    _data = x.get("pattern")

                    for w in creds:
                        w = w["w3c"]
                        if not x.get("pattern") and x.get("type"):
                            if sub and w.get(root, {}).get(sub):
                                print("Hello")
                                cred_id.append(w["id"])
                            elif w.get(root):
                                print("Hello")
                                cred_id.append(w["id"])
                        elif _data:
                            if sub and w.get(root, {}).get(sub) == _data:
                                print("Hello")
                                cred_id.append(w["id"])
                            elif w.get(root) == _data:
                                print("Hello")
                                cred_id.append(w["id"])

            return jsonify(list(set(cred_id))), 200

        @self.app.route("/send_credential",methods=['POST'])
        def __send_cred__():
            data =request.json
            if data:
                attachments = data["attachments"][0]["data"]["json"]
                _from = data["from"]
                to = data["to"]
                to_key = attachments["credentialSubject"]["id"]
                Q = Query()
                tb = TinyDB("../../src/Wallet/db.json")
                print(to_key)
                data = tb.search(Q.pub_key == to_key)
                data_creds = data[0]["creds"]
                data_creds.append({"w3c":attachments,"disc":[],"raw":[],"type":"ZKP"})
                tb.update({"creds":data_creds},Q.pub_key==to_key)
                



        @self.app.route("/receive_presentation", methods=["POST"])
        def __receive__():
            _data = request.json
            qr = tinydb.Query()
            tn = tinydb.TinyDB("../../src/Wallet/db.json")
            _pl = tn.all()[0]
            _didK = _pl["pub_key"]
            _peers = _pl["peers"]
            for p in _peers:
                if p["their_did"] == _data["from"]:
                    My_did = p["my_did"]
            if _data["to"] == My_did:
                _payload = _data["attachments"][0]["data"]["json"]
                _payload["from"] = _data["from"]
                req = _pl["request"]
                req.append({"status": "Pending", "data": _payload})

                tn.update({"request": req}, qr.pub_key == _didK)

            return Response({"d": "s"}, 200)

        @self.app.route("/presentation_result")
        def __presentation_result__(self):
            data = request.json
            qr = tinydb.Query()
            tn = tinydb.TinyDB("../../src/Wallet/db.json")
            _pl = tn.all()[0]
            _pub_key = _pl["pub_key"]
            if data:
                if data["verified"]:
                    reqs = _pl["request"]
                    for x in reqs:
                        if x["data"]["id"] == data["id"]:
                            x["status"] = "Accepted"
                            break
                    tn.update({"request": reqs}, qr.pub_key == _pub_key)
                    return Response("Done", 200)

        @self.app.route("/send_presentation", methods=["POST"])
        def __send_presentation__():
            print("***********")
            data = request.json
            tn = tinydb.TinyDB("../../src/Wallet/db.json")
            _pl = tn.all()[0]
            _didK = _pl["pub_key"]
            _peers = _pl["peers"]
            for p in _peers:
                if p["their_did"] == data["from"]:
                    My_did = p["my_did"]

            from did_peer_4 import resolve

            _decoded = resolve(p["their_did"])
            print(p["their_did"])
            uri = _decoded["service"][0]["serviceEndpoint"]["uri"]
            uri = uri + "/accept_credential/defi"
            print(uri)
            did_comm = {
                "id": str(uuid4()),
                "type": SEND_PRESENTATION,
                "from": My_did,
                "body": {
                    "goal_code": SEND_PRESENTATION_TYPE,
                    "goal": "Message To Send Presentation",
                    "accept": ["didcomm/v2", "didcomm/aip2;env=rfc587"],
                },
                "attachments": [
                    {
                        "id": str(uuid4()),
                        "media_type": "application/json",
                        "data": {"json": data},
                    }
                ],
            }

            _r = requests.post(uri, json=did_comm)

            return Response("sended", 200)

        @self.app.route(PING, methods=["POST"])
        def __pong__():
            _payload = request.json
            _payload = json.loads(_payload)
            if _payload:
                print("Connection Setuped")
                return Response(":)", 200)

    def start(self):
        self.__setup_init_connection_routes__()
        self.app.run(host="127.0.0.1", port=self.port, debug=True)


if __name__ == "__main__":
    isuer = Holder(5001)
    isuer.start()
