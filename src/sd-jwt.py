import flask
from flask import request,Response
import uuid
import logging
from flask_cors import CORS
import json
import base64
from key import Key
import secrets
import hashlib
from cryptography.hazmat.primitives import serialization
import binascii

lg = logging.getLogger("test")

app = flask.Flask(__name__)

CORS(app)

def base64url_decode(data: bytes) -> str:
    return base64.urlsafe_b64decode(data + b'==').decode("utf-8")


class Sd_Jwt:
    def __init__(self) -> None:
        pass

    @app.route("/get_sd_jwt", methods=["POST"])
    def getdata():
        header = {
            "alg": "ES256",
            "kid": uuid.uuid4().hex,
            "typ": "vc+ld+json+sd-jwt",
            "cty": "vc+ld+json",
        }
        payload = request.data
        payload = json.loads(payload)
        
        with open('blockchain_DIDs.json') as F:
            _key_registery = json.loads(F.read())

        for k in _key_registery['keys']:
            if k['did'] == payload['issuer']:
                private_key = k['private_key']
                break


        KEY_P = Key(location='/',loaded_private=private_key)
        DIS = []

        def base64url_encode(data: bytes) -> str:
            return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

        def generate_salt(length: int = 16) -> bytes:
            salt_bytes = secrets.token_bytes(length)
            return base64url_encode(salt_bytes)

        def process_sd_digest(data: dict, ky: None):
            _sd = []
            _rety = {}
            DIS = []

            for k, v in data.items():
                if isinstance(v, dict):
                    values = process_sd_digest(v, k)
                    _rety[k] = values
                else:
                    salt = generate_salt()
                    item_str = base64url_encode(
                        str([salt, f"{ky}/{k}" if ky else k, v]).encode("utf-8")
                    )
                    DIS.append(item_str)
                    _sha = hashlib.sha3_256()
                    _sha.update(item_str.encode("utf-8"))
                    _sd.append(_sha.hexdigest())
                    #print(_sha.hexdigest())

            if ky:
                return _sd
            else:
                _rety["_sd"] = _sd
                return _rety, DIS

        _process = process_sd_digest(payload["credentialSubject"], ky=None)

        payload["credentialSubject"] = _process[0]

        payload["_sd_alg"] = "sha-256"
        # OKP CUZ it is Ed25519
        payload["cnf"] = {
            "jwk": {
                "kty": "OKP",
                "crv": "Ed25519",
                "x": KEY_P.__get_jwk_OKP_pub__(),
            }
        }

        header = base64url_encode(json.dumps(header).encode("utf-8"))
        payload = base64url_encode(json.dumps(payload).encode("utf-8"))
        print(f"{header}.{payload}")
        _top = f"{header}.{payload}"
        _signature = KEY_P.sign(_top.encode("utf-8")).hex()

        _top = f"{_top}.{_signature}"
        _final_str = ""
        for x in _process[1]:
            _final_str = _final_str + "~" + x

        return Response(f"{_top}{_final_str}",status=200)

    @app.route("/validate", methods=["POST"])
    def validate():
        print(request.data)
        _sd_jwt = request.data.decode().split(".")
        _header = _sd_jwt[0]
        _payload = _sd_jwt[1]
        _signature = _sd_jwt[2].split("~")[0]
        _disc = _sd_jwt[2].split("~")[1:]
    
        _header = base64url_decode(_header.encode("utf-8"))

        _payload = json.loads(base64url_decode(_payload.encode("utf-8")))
        # Validate
        if "VerifiableCredential" in _payload["type"]:
            issuer = _payload["issuer"]
            issuance = _payload["validFrom"]
            expires = _payload["validUntil"]
            #expires = datetime.strptime(expires, "%Y-%m-%d")
            #now = datetime.now()
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

                            _signature = binascii.unhexlify(_signature)
                            print(pub_key.public_bytes(
                                        encoding=serialization.Encoding.Raw,
                                        format=serialization.PublicFormat.Raw,
                                    )
                                    .hex())
                            print()
                            try:
                                pub_key.verify(_signature, f"{_sd_jwt[0]}.{_sd_jwt[1]}".encode("utf-8"))
                                return Response("", 200)
                                print("Signature is valid.")
                            except Exception as e:
                                print("Signature verification failed:", e)
                                return Response("", 400)
                        elif crv == "p-384":
                            #TODO
                            pass
                        elif crv == "p-512":
                            #TODO
                            pass

        


ss = Sd_Jwt()
app.run("0.0.0.0", 3000, debug=True)
