import ecdsa.ellipticcurve
import flask
from flask_cors import CORS
from flask import request, Response

from tinydb import TinyDB,Query
import sys
import os
from cryptography.hazmat.primitives import serialization


sys.path.append("../")
from key import Key
import binascii
import json
import base58
import base64
import secrets
import hashlib
from datetime import datetime

WALLET_PORT = 5003
app = flask.Flask(__name__)

CORS(app)


def hex_to_did_key_secp256k1(hex_public_key):
    public_key_bytes = bytes.fromhex(hex_public_key)
    multicodec_prefix = bytes([0xE7])
    prefixed_key = multicodec_prefix + public_key_bytes
    did_key = "z" + base58.b58encode(prefixed_key).decode("utf-8")
    return did_key


class Wallet:
    def __init__(self, name, crypto_ecda):
        self.db = TinyDB("db.json")
        self.name = name

        key, algo = self.key_generate(crypto_ecda)
        key = hex_to_did_key_secp256k1(key)
        self.db.insert(
            {"name": name, "alg": algo, "pub_key": f"did:key:{key}", "creds": [],"peers":[],"request":[]}
        )

    def key_generate(self, crypt):
        keyp = Key(location=os.path.join('Key/'))
        public_key = keyp.get_pub()
        return public_key, str(crypt)


def base64url_decode(data: bytes) -> str:
    return base64.urlsafe_b64decode(data + b'==').decode("utf-8")


@app.route("/create", methods=["POST"])
def __create__():
    if not os.path.exists(os.path.join('Key/')):
        os.makedirs(os.path.join('Key/'))
    _ = Wallet("Test", crypto_ecda=ecdsa.SECP256k1)
    return Response("", 200)


@app.route("/sign",methods=["POST"])
def __sign__():
    data = request.json
    with open('Key/holder_key.json') as F:
        _key_registery = json.loads(F.read())


    KEY_P = Key(location='/',loaded_private=_key_registery["private_key"])
    _signature = KEY_P.sign(str(data["payload"]).encode("utf-8")).hex()

    return Response(_signature,200)

@app.route("/validate", methods=["POST"])
def validate():
    _data = request.data.decode()
    _data = json.loads(_data)
    _sd_jwt = _data["data"].split(".")
    _header = _sd_jwt[0]
    _payload = _sd_jwt[1]
    _signature = _sd_jwt[2].split("~")[0]
    _disc = _sd_jwt[2].split("~")[1:]
    _key = _data["my_key"]
    print(_key)
    _header = base64url_decode(_header.encode("utf-8"))

    _payload = json.loads(base64url_decode(_payload.encode("utf-8")))
    # Validate
    if "VerifiableCredential" in _payload["type"]:
        issuer = _payload["issuer"]
        issuance = _payload["validFrom"]
        expires = _payload["validUntil"]
        #expires = datetime.strptime(expires, "%Y-%m-%d")
        now = datetime.now()
        if 1>2:
            return Response("Credential Expores", 401)
        else:
            cnf = _payload["cnf"]
            if cnf["jwk"]:
                kty = cnf["jwk"]
                if kty["kty"] == "OKP":
                    crv = kty["crv"]
                    x = kty["x"]
                    # Curve Conditioning ---- p-256 , p-384 , p-512
                    if crv == "Ed25519":
                        pub_key = Key.load_ed25519_public_key_from_OKP_jwk(x)
                        _digest = f"{_sd_jwt[0]}.{_sd_jwt[1]}".encode("utf-8")
                        _sha = hashlib.sha256()
                        _sha.update(_digest)
                        _signature = binascii.unhexlify(_signature)
                        print(pub_key.public_bytes(
                                    encoding=serialization.Encoding.Raw,
                                    format=serialization.PublicFormat.Raw,
                                )
                                .hex())
                        if not pub_key.verify(
                            _signature,
                            data=f"{_sd_jwt[0]}.{_sd_jwt[1]}".encode("utf-8"),
                        ):
                            _is_digest_contains = True
                            for _d in _disc:
                                sh = hashlib.sha3_256()
                                sh.update(_d.encode("utf-8"))
                                if sh.hexdigest() in base64url_decode(
                                    _sd_jwt[1].encode("utf-8")
                                ):
                                    pass
                                else:
                                    _is_digest_contains = False
                                    break
                            if _is_digest_contains:
                                Q = Query()
                                tb = TinyDB("db.json")
                                data = tb.search(Q.pub_key == _key)
                                print(data)
                                creds = data[0]["creds"]
                                creds.append({"w3c":_payload,"disc":_disc,"raw":_data,"type":"Normal"})
                                tb.update({"creds":creds},Q.pub_key==_key)

                        else:
                            print("do")

                    elif crv == "p-384":
                        #TODO
                        pass
                    elif crv == "p-512":
                        #TODO
                        pass

    return Response("", 200)


@app.route("/is_exsist", methods=["GET"])
def __check__():
    db = TinyDB("db.json")
    return Response(str(db.all()), status=200)


app.run(port=WALLET_PORT, debug=True)
