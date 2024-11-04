from uuid import uuid4
from dataclasses import dataclass, asdict
from typing import List, Collection
import json
from CONST.CHEQNETDID import *


@dataclass
class Presentation_Scheme:
    id: str
    input_descriptors: Collection
    submission_requirements: Collection


@dataclass
class Input_descriptors_scheme:
    id: str
    name: str
    group: Collection
    purpose: str
    constraints: dict


@dataclass
class SubReq:
    name: str
    rule: str
    count: int
    _from: str


class Presentation_DEF:
    def __init__(self):
        pass

    def __create__(self):
        _template = dict()

        _format = {
            "jwt": {"alg": ["EdDSA", "ES256K", "ES384"]},
            "jwt_vc": {"alg": ["ES256K", "ES384"]},
            "jwt_vp": {"alg": ["EdDSA", "ES256K"]},
        }

        _constrains = {
            "fields": [
                {
                    "path": ["$.type"],
                    "filter": {
                        "type": "array",
                        "contains": {
                            "type": "string",
                            "pattern": "GovermentIdCredential",
                        },
                    },
                },
                {
                    "path": ["$.credentialSubject.governmentIDNumber"],
                },
                {
                    "path": ["$.issuer"],
                    "filter": {
                        "type": "string",
                        "pattern": GOV_ID_PROVIDER,
                    },
                },
            ]
        }
        _sub_req = {"name": "Goverment Id Data", "rule": "all", "from": "main"}

        _inp_descriptor = Input_descriptors_scheme(
            str(uuid4()), "Please Submmit", ["main"], "Just Kidding", _constrains
        )

        _pr_def = Presentation_Scheme(str(uuid4()), [asdict(_inp_descriptor)], _sub_req)
        return asdict(_pr_def)

    def __create_defi__(self):
      

        _constrains = {
            "fields": [
                {
                    "path": ["$.type"],
                    "filter": {
                        "type": "array",
                        "contains": {
                            "type": "string",
                            "pattern": "PersonHoodCredential",
                        },
                    },
                },
                {
                    "path": ["$.credentialSubject.biometrics"],
                },
                {
                    "path": ["$.issuer"],
                    "filter": {
                        "type": "string",
                        "pattern": BIOMETRICS_PROVIDER,
                    },
                },
            ]
        }
        _sub_req = {"name": "PHC Credential Data", "rule": "all", "from": "main"}

        _inp_descriptor = Input_descriptors_scheme(
            str(uuid4()), "Please Submmit Your Personhood Credential", ["main"], "Provide to use defi platform", _constrains
        )

        _pr_def = Presentation_Scheme(str(uuid4()), [asdict(_inp_descriptor)], _sub_req)
        return asdict(_pr_def)


ll = Presentation_DEF()
ll.__create__()
