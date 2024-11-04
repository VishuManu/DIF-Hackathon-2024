import ecdsa.ellipticcurve
import flask
from flask_cors import CORS
from flask import request, Response
import ecdsa
from ecdsa import Ed25519, SECP256k1
from ecdsa.keys import VerifyingKey
from ecdsa.keys import PointJacobi
from tinydb import TinyDB,Query
import sys

sys.path.append("../")
from key import Key
import binascii
import json
import base58
import base64
import secrets
import ecdsa
import hashlib
from ecdsa.util import string_to_number
from datetime import datetime

VERF_WALLET_PORT = 5005
app = flask.Flask(__name__)

CORS(app)


def hex_to_did_key_secp256k1(hex_public_key):
    public_key_bytes = bytes.fromhex(hex_public_key)
    multicodec_prefix = bytes([0xE7])
    prefixed_key = multicodec_prefix + public_key_bytes
    did_key = "z" + base58.b58encode(prefixed_key).decode("utf-8")
    return did_key


class Verifier_WL:
    def __init__(self, name, crypto_ecda,mode):
        json = "../DB/defi.json" if mode == "defi" else "../DB/biometrics.json"
        self.db = TinyDB(json)
        self.name = name

        key, algo = self.key_generate(crypto_ecda)
        key = hex_to_did_key_secp256k1(key)
        self.db.insert(
            {"name": name, "alg": algo, "pub_key": f"did:key:{key}", "creds": [],"peers":[]}
        )

    def key_generate(self, crypt):
        keyp = Key(curve=crypt)
        public_key = keyp.get_pub().to_string().hex()
        return public_key, str(crypt)


def base64url_decode(data: bytes) -> str:
    return base64.urlsafe_b64decode(data + b'==').decode("utf-8")


@app.route("/create/<mode>", methods=["POST"])
def __create__(mode):
    _ = Verifier_WL("Test", crypto_ecda=ecdsa.SECP256k1,mode=mode)
    return Response("", 200)



@app.route("/sign",methods=['POST'])
def __sign__():
    data = request.json
    with open('../../src/blockchain_DIDs.json') as F:
        _key_registery = json.loads(F.read())

    for k in _key_registery['keys']:
        if k['did'] == data["from"]:
            private_key = k['private_key']
            break

    KEY_P = Key(location='/',loaded_private=private_key)
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
    _header = base64url_decode(_header.encode("utf-8"))

    _payload = json.loads(base64url_decode(_payload.encode("utf-8")))
    # Validate
    if "VerifiableCredential" in _payload["type"]:
        issuer = _payload["issuer"]
        issuance = _payload["issuanceDate"]
        expires = _payload["expirationDate"]
        expires = datetime.strptime(expires, "%Y-%m-%d")
        now = datetime.now()
        if expires > now:
            return Response("Credential Expores", 401)
        else:
            cnf = _payload["cnf"]
            if cnf["jwk"]:
                kty = cnf["jwk"]
                print(now)

                if kty["kty"] == "EC":
                    crv = kty["crv"]
                    x = kty["x"]
                    y = kty["y"]
                    # Curve Conditioning ---- p-256 , p-384 , p-512
                    if crv == "p-256" or crv == "SECP256k1":
                        pub_key = VerifyingKey.from_public_point(
                            ecdsa.ellipticcurve.Point(SECP256k1.curve, x, y),
                            curve=SECP256k1,
                        )
                        _digest = f"{_sd_jwt[0]}.{_sd_jwt[1]}".encode("utf-8")
                        _sha = hashlib.sha256()
                        _sha.update(_digest)
                        _signature = binascii.unhexlify(_signature)
                        if pub_key.verify(
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
                                data = tb.search(Q.pub__key == _key)
                                print(data)
                                tb.update({"creds":[{"w3c":_payload,"disc":_disc,"raw":_data}]},Q.pub_key==_key)


                    elif crv == "p-384":
                        # TODO To Be Work On
                        pass
                    elif crv == "p-512":
                        # TODO To Be Work On
                        pass

    return Response("", 200)


@app.route("/get_data/<mode>", methods=["GET"])
def __check__(mode):
    qr = Query()
    json = "../DB/defi.json" if mode == "defi" else "../DB/biometrics.json"
    db = TinyDB(json)
    print(db.all())
    return Response(str(db.all()), status=200)


app.run(port=VERF_WALLET_PORT, debug=True)
