from enum import Enum
import sys
import urllib
import base64
import qrcode
import qrcode.image.pil
import hashlib

sys.path.append("../")
from CONST.CONST import *
from CONST.GOAL_C import *
from presentation_defination import Presentation_DEF
import os
import numpy as np
from werkzeug.utils import secure_filename
from fingerprint import Fingerprint
import ipfshttpclient
import itertools
import httpx
import asyncio

# from Test.did_generate import generate2
from CONST.TYPE import *
from CONST.ZKP_TYPE import *
from CONST.CHEQNETDID import *
from Utils.didcommv2_message_templates import Template
import json
import asyncio
import aiohttp
import logging
from flask import Flask, redirect, url_for, jsonify, flash, request, Response
import requests
from did.peer import Peer_DID
from uuid import uuid4
from flask_cors import CORS
import tinydb
from datetime import datetime


class Initial_Invitation_Sending_Medium(Enum):
    QR = 0
    URL = 1
    BLUETOOTH = 2


class Verifier:
    def __init__(self) -> None:
        self.api_key = "xxxxxx"
        self.app = Flask(__name__)
        CORS(self.app)
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)
        self.name = "ABC Verifier organisation"
        self.init_did = "did:key:z789456"
        self.presentation_def = Presentation_DEF()
        self.req_template = Template()
        self.verifier_agent_url = "http://127.0.0.1:5000"
        self.receiver_data = {}
        self.prefered_invitation_type = Initial_Invitation_Sending_Medium.URL
        self.UPLOAD_FOLDER = "uploads"  # Directory where images will be saved
        self.ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

        # Ensure the upload folder exists
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

        # Function to check allowed file extensions

    def allowed_file(self, filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS
        )

    def __get_agent__(self):
        return self.verifier_agent_url

    def __setup_initial__connection_listener__(self):
        # STEP 1 FOR ALL PROVER
        @self.app.route(CREATE_INVITATION + "/<org>", methods=["GET"])
        def __initiate_connection_request__(org) -> qrcode.image.pil.PilImage | str:
            # generating invitation url or QR
            _T = Template()
            _D = _T.__create_invitation__(
                self.name, self.init_did, self.verifier_agent_url
            )
            encoded = base64.urlsafe_b64encode(str(_D).encode("utf-8"))
            if self.prefered_invitation_type == Initial_Invitation_Sending_Medium.URL:
                return f"{self.verifier_agent_url}/invite_url?_oob={encoded.decode('utf-8')}&type={org}"
            else:
                qr = qrcode.make(encoded)
                qr.save("qr.png")
                return qr

        @self.app.route(RECEIVE_INVITATION + "/" + "<_type>", methods=["POST"])
        def __receive_peer_did_and_connection__(_type):
            # ACCEPT RESPONSE AND GENERATE PEER
            # TODO Decode JWT , JWS , JWM of Cipher text
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

                            from did_peer_4 import resolve

                            _decoded_peer = resolve(_received_peer)

                            if _received_peer is None:
                                return "No"

                            # TODO decoding peer did fetching URLs of endpoint
                            server_uri = (
                                _decoded_peer["service"][0]["serviceEndpoint"]["uri"]
                                if _decoded_peer["service"]
                                else None
                            )
                            self.receiver_data[_received_peer] = server_uri
                            server_uri = server_uri + RECEIVE_PEER_EXCHANGE_RESPONSE
                            template = Template()
                            # TODO : Generating Peer DID from wallet
                            from Peer.did_generate import generate2, generate3

                            if _type == "defi":
                                _peer_created = generate2()
                            else:
                                _peer_created = generate3()
                            _DB = (
                                "../DB/defi.json"
                                if _type == "defi"
                                else "../DB/biometrics.json"
                            )
                            tn = tinydb.TinyDB(_DB)
                            _date = datetime.now()
                            _unq = str(uuid4())
                            tn.insert(
                                {
                                    "peers": {
                                        "connection_id": _unq,
                                        "my_did": _peer_created,
                                        "their_connection_id": request.json["conid"],
                                        "their_did": _received_peer,
                                        "status": "peer_sent",
                                        "createdAt": str(_date),
                                    }
                                }
                            )

                            _json_test = template.__invitation_response__(
                                "Me", _peer_created, _decoded["to"], _decoded["id"]
                            )
                            _client = requests.post(
                                server_uri,
                                json={
                                    "mycid": _unq,
                                    "ycid": request.json["conid"],
                                    "data": json.dumps(_json_test),
                                },
                            )
                            if _client.status_code == 200:
                                self.log.log(
                                    level=1,
                                    msg=f"My Peer DID {_peer_created} Sent to {_decoded['to']} holder of credential",
                                )
                            else:
                                self.log.error(
                                    f"Unable to sent Peer DID to holder due to {_client.status_code} status code in request"
                                )

                            return "Yo"
                            # self.__send_my_peer__(server_uri,_received_peer,pthid=_decoded["pthid"])
                            # TODO SAVE Peer to wallet with connection

                        else:
                            return "no"
                    else:
                        return "nop"
            else:
                return "No"

        @self.app.route("/send_zkp_proof_request")
        def __send_zkp__():
            data = request.json
            to = data["to"]
            _from = ""
            req_template = Template()
            req = req_template.zkp_request(
                {"to": to, "from": _from, "cred_id": data["cred_id"]}
            )

            from did_peer_4 import resolve

            doc = resolve(to)
            doc["service"][0]["serviceEndpoint"]["uri"]

        @self.app.route("/create_biometric_credential", methods=["POST"])
        async def __ask_fingerprint__():
            uploaded_file = request.files["file"]
            if uploaded_file.filename != "":
                from did import peer

                peer_did = peer.Peer_DID(request.form["to_peer"])
                if peer_did.__validate__():
                    uploaded_file.save(uploaded_file.filename)
                    fr = Fingerprint()
                    ls = fr.__generate__(uploaded_file.filename)
                    import math

                    _bifu = []
                    for x in ls["bifurcations"]:
                        lst = x[:2] + x[2]
                        lst = [x if not math.isnan(x) else 0.0 for x in lst]
                        _bifu.append(lst)

                    _term = []
                    for x in ls["terminations"]:
                        lst = x[:2] + x[2]
                        lst = [x if not math.isnan(x) else 0.0 for x in lst]
                        _term.append(lst)

                    _bifu = [abs(x) for x in list(itertools.chain.from_iterable(_bifu))]
                    _final = _bifu.extend(_term)

                    session_id = str(uuid4())
                    response = requests.post(
                        "http://localhost:5010/execute_circuit",
                        json={
                            "session": session_id,
                            "_16nodes_biometrics_merkel": [
                                1,
                                2,
                                3,
                                4,
                                5,
                                6,
                                7,
                                8,
                            ],
                            "zkp_type": "digest_pre_image_proof",
                        },
                    )
                    import time

                    while not os.path.exists(
                        os.path.join("SnarkJS", "Sessions", session_id, "proof.json")
                    ):
                        time.sleep(1)

                    # Read the proof file
                    with open(
                        os.path.join("SnarkJS", "Sessions", session_id, "proof.json"),
                        "r",
                    ) as F:
                        proof = F.read()

                    # Read the verification file
                    with open(
                        os.path.join(
                            "SnarkJS", "Sessions", session_id, "verification_key.json"
                        ),
                        "r",
                    ) as F:
                        verification = F.read()

                    with open(
                        os.path.join("SnarkJS", "Sessions", session_id, "public.json"),
                        "r",
                    ) as F:
                        public = F.read()
                    w3c_phc_json = {
                        "@context": ["https://www.w3.org/ns/credentials/v2"],
                        "id": str(uuid4()),
                        "type": ["VerifiableCredential", "PersonhoodCredential"],
                        "issuer": request.form["issuer"],
                        "validFrom": "2024-01-01",
                        "validUntil": "2024-12-12",
                        "credentialSubject": {
                            "id": request.form["to_key"],
                            "biometrices": {
                                "_zkp": {
                                    "_public_data": json.loads(public),
                                    "circuit": {
                                        "proof": json.loads(proof),
                                        "verification": json.loads(verification),
                                        "curve": "bn128",
                                    },
                                }
                            },
                        },
                        "credentialStatus": [
                            {
                                "id": "test",
                                "type": "StatusList2021Entry",
                                "statusPurpose": "revocation",
                                # Just for demonstartion
                                "statusListIndex": 45,
                            },
                            {
                                "id": "test",
                                "type": "StatusList2021Entry",
                                "statusPurpose": "suspension",
                                # Just for demonstartion
                                "statusListIndex": 78,
                            },
                        ],
                    }

                    _sign = requests.post(
                        "http://localhost:5005/sign",
                        json={"from": BIOMETRICS_PROVIDER, "payload": w3c_phc_json},
                    )
                    w3c_phc_json["proof"] = {
                        "type": "DataIntegrityProof",
                        "cryptosuite": "eddsa-rdfc-2022",
                        "created": "2021-11-13T18:19:39Z",
                        "verificationMethod": "https://university.example/issuers/14#key-1",
                        "proofPurpose": "assertionMethod",
                        "proofValue": _sign.content.decode(),
                    }
                    from did_peer_4 import resolve

                    resolved = resolve(request.form["to_peer"])
                    _didcommmessage = {
                        "type": "https://didcomm.org/out-of-band/2.0/invitation",
                        "id": str(uuid4()),
                        "from": request.form["issuer"],
                        "to": request.form["to_peer"],
                        "body": {
                            "goal_code": SEND_CREDENTIAL,
                            "goal": "Message To Ask For Presentation",
                            "accept": ["didcomm/v2", "didcomm/aip2;env=rfc587"],
                        },
                        "attachments": [
                            {
                                "id": str(uuid4()),
                                "media_type": "application/json",
                                "data": {"json": w3c_phc_json},
                            }
                        ],
                    }

                    _r = requests.post(
                        resolved["service"][0]["serviceEndpoint"]["uri"]
                        + "/send_credential",
                        json=_didcommmessage,
                    )

                    # _cid['Hash']

                    return jsonify(
                        {
                            "credential": "Done",
                        }
                    ), 200

                else:
                    return Response("Not A Valid Did", 403)

        @self.app.route("/accept_credential/<mode>", methods=["POST"])
        def __accept_cred__(mode):
            _json = request.json
            qr = tinydb.Query()
            _DB = "../DB/defi.json" if mode == "defi" else "../DB/biometrics.json"
            tn = tinydb.TinyDB(_DB)
            all_data = tn.search(qr.id == "1234") if mode == "defi" else tn.all()
            attachments = _json["attachments"][0]["data"]["json"]
            if _json:
                if _json["type"] == SEND_PRESENTATION:
                    if _json["body"]["goal_code"] == SEND_PRESENTATION_TYPE:
                        _shared_id = attachments["request_id"]

                        '''_sended = all_data[0]["sended_request"]
                        for s in _sended:
                            for inp_des in s["input_descriptors"]:
                                if inp_des["id"] == _shared_id:
                                    _ = s
                                    break'''

                        if 1==1:
                            is_ok = False
                            cred = attachments["cred"]
                            for VCs in cred["verifiableCredential"]:
                                if "value" in VCs.keys():
                                    # ZKP CASE
                                    w3c = VCs["value"]
                                    if w3c["issuer"] == BIOMETRICS_PROVIDER:
                                        subject = w3c["credentialSubject"]
                                        if subject["biometrices"]["_zkp"]:
                                            zkp = subject["biometrices"]["_zkp"]
                                            _path = os.path.join(
                                                "ZKP_Verfication", str(uuid4())
                                            )
                                            os.makedirs(_path)
                                            with open(
                                                os.path.join(_path, "proof.json"), "w+"
                                            ) as prf:
                                                prf.write(
                                                    json.dumps(zkp["circuit"]["proof"])
                                                )

                                            with open(
                                                os.path.join(
                                                    _path, "verification_key.json"
                                                ),
                                                "w+",
                                            ) as ver:
                                                ver.write(
                                                    json.dumps(
                                                        zkp["circuit"]["verification"]
                                                    )
                                                )

                                            with open(
                                                os.path.join(_path, "public.json"),
                                                "w+",
                                            ) as ver:
                                                ver.write(
                                                    json.dumps(zkp["_public_data"])
                                                )

                                            _d = {
                                                "cwd": os.path.join("../", "../", _path)
                                            }
                                            import subprocess

                                            s = subprocess.getstatusoutput(
                                                f"snarkjs groth16 verify {os.path.join(_path,"verification_key.json")} {os.path.join(_path,"public.json")} {os.path.join(_path,"proof.json")}"
                                            )
                                            if s[0] == 0:
                                                if "OK" in s[1]:
                                                    tn.update({"verified":True})
                                                    return Response("Done",200)

                                else:
                                    if (
                                        VCs["type"]
                                        == "EnvelopedVerifiableCredential"
                                    ):
                                        _data = VCs["id"]
                                        if "data:application/vc+sd-jwt," in _data:
                                            _data = _data.replace(
                                                "data:application/vc+sd-jwt,", ""
                                            )
                                                
                                            _check = requests.post("http://localhost:3000/validate",_data)
                                            print(_check)
                                            if (_check.status_code == 200):
                                                return Response("Ok",200)
                                

        @self.app.route("/ask_presentation/<mode>/<peer>", methods=["POST"])
        async def __ask__(peer, mode):
            from did_peer_4 import resolve

            _decoded = resolve(peer)
            qr = tinydb.Query()
            _DB = "../DB/defi.json" if mode == "defi" else "../DB/biometrics.json"
            tn = tinydb.TinyDB(_DB)
            for x in tn.all():
                if x["peers"]["their_did"] == peer:
                    _pl = x["peers"]
            print(_pl)
            if _decoded:
                _data = {
                    "from": _pl["my_did"],
                    "to": peer,
                    "payload": self.presentation_def.__create__()
                    if mode == "biometrics"
                    else self.presentation_def.__create_defi__(),
                }

                tn.update(
                    {
                        "sended_request": [
                            self.presentation_def.__create__()
                            if mode == "biometrics"
                            else self.presentation_def.__create_defi__()
                        ]
                    },
                    qr.id == "1234",
                )

                try:
                    response = requests.post(
                        f"{_decoded["service"][0]["serviceEndpoint"]["uri"]}/receive_presentation",
                        json=self.req_template.__presentation_msg__(_data),
                    )

                    return jsonify(self.req_template.__presentation_msg__(_data)), 200
                except Exception as E:
                    return Response(str(E), 500)

        @self.app.route(PING, methods=["POST"])
        def __trust_ping__():
            _payload = json.loads(request.json)
            if _payload:
                if _payload["type"] == PING_URL:
                    _from = _payload["from"]
                    _body = _payload["body"]
                    if _body and _from:
                        self.log.log(level=1, msg="Ping Reponse Accepted")
                        # TODO searching for from in wallet
                        if self.receiver_data[_from]:
                            service_endpoint = self.receiver_data[_from] + PING
                        if _body["response_requested"]:
                            response = {
                                "type": PING_REPONSE_URL,
                                "id": str(uuid4()),
                                "thid": _payload["id"],
                            }

                            response = json.dumps(response)
                            _ = requests.post(service_endpoint, json=response)
                            return Response("Last Interactio Done from Verfier", 200)
                            # if result.status_code == 200:
                            #    self.log.log(1,f"Trust Ping Sent Successfully")
                            #    return result
                            # else:
                            #    self.log.error("Failed To send Ping Response")

    def __initiate_flask__(self):
        self.__setup_initial__connection_listener__()
        self.app.secret_key = "AZDSSS"
        self.app.run(host="127.0.0.1", port=5000)


V = Verifier()
V.__initiate_flask__()
