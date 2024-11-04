import typing
from enum import Enum
import json

class DID_METHODS(Enum):
    WEB = "did:web"
    PEER = "did:peer"
    SOV = "did:sov"
    ETH = "did:eth"
    BTCR = "did:btcr"
    COM  = "did:com"
    ONT = "did:ont"

    SELFKEY = "did:selfkey"
    META = "did:meta"
    CELO = "did:celo"
    ETHO = "did:etho"
    ION = "did:ion"
    POLYGON = "did:polygon"
    JOLO = "did:jolo"
    BNB = "did:bnb"
    SOL = "did:sol"
    KILT = "did:kilt"
    DOCK = "did:dock"
    KEY = "did:key"
    INDY ="did:indy"


class verf_type(Enum):
    publicKeyJwk = "publicKeyJwk",
    publicKeyMultibase = "publicKeyMultibase"


class DID:
    def __init__(self) -> None:
        self.methods = ''
        self.context = []
        self.id:str = None
        self.keyAgreement = []
        self.assertionMethod = []
        self.controller:typing.List = []
        self.alsoKnownAs:typing.Optional[str]
        self.verificationMethod:typing.List = []
        self.authentication = []
        self.capabilityInvocation = []
        self.service = []
        

    def __parse__(self,did:str):
        # getting did ->
        if did:
            splitted = did.split(":")
            self.context = ["https://www.w3.org/ns/did/v1"]
            if len(splitted) >= 3:
                first_two = f"{splitted[0]}:{splitted[1]}"
                print(first_two)
                self.id = did
                self.controller = [self.id]


    def __context__(self):
        pass

    def __diddoc__(self):
        _diddoc = {
            "@context":self.context,
            "id":self.id,
            "verificationMethod":self.verificationMethod,
            "authentication":self.authentication,
            "assertionMethod":self.assertionMethod,
            "capabilityInvocation":self.capabilityInvocation,
            "controller":self.controller[0] if len(self.controller) == 1 else self.controller,
            "service":self.service
        }

        return json.dumps(_diddoc)

d = DID()
d.__parse__("did:peer:xcvwwwwq")
print(d.__diddoc__())