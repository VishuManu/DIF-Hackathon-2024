from did_peer_4 import encode


def generate():
    _data = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1",
        ],
        "verificationMethod": [
            {
                "id": "#key-0",
                "type": "Multikey",
                "publicKeyMultibase": "z6MkqRYqQiSgvZQdnBytw86Qbs2ZWUkGv22od935YF4s8M7V",
            },
            {
                "id": "#key-1",
                "type": "Multikey",
                "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc",
            },
        ],
        "authentication": ["#key-0"],
        "capabilityDelegation": ["#key-0"],
        "service": [
            {
                "id": "#didcomm-0",
                "type": "DIDCommMessaging",
                "serviceEndpoint": {
                    "uri": "http://localhost:5001",
                    "accept": ["didcomm/v2"],
                },
            }
        ],
        "keyAgreement": ["#key-1"],
    }

    return encode(_data)


def generate3():
    _data = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1",
        ],
        "verificationMethod": [
            {
                "id": "#key-0",
                "type": "Multikey",
                "publicKeyMultibase": "z6MkqRYqQiSgvZQdnBytw86Qbs2ZWUkGv22od935YF4s8M7V",
            },
            {
                "id": "#key-1",
                "type": "Multikey",
                "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc",
            },
        ],
        "authentication": ["#key-0"],
        "capabilityDelegation": ["#key-0"],
        "service": [
            {
                "id": "#didcomm-0",
                "type": "DIDCommMessaging",
                "serviceEndpoint": {
                    "uri": "http://localhost:5000",
                    "accept": ["didcomm/v2"],
                },
            }
        ],
        "keyAgreement": ["#key-1"],
    }

    return encode(_data)


def generate2():
    _data = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1",
        ],
        "verificationMethod": [
            {
                "id": "#key-0",
                "type": "Multikey",
                "publicKeyMultibase": "z6MkqRYqQiSgvZQdnBytw86Qbs2ZWUkGv22od935YF4s8M7V",
            },
            {
                "id": "#key-1",
                "type": "Multikey",
                "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc",
            },
        ],
        "authentication": ["#key-0"],
        "capabilityDelegation": ["#key-0"],
        "service": [
            {
                "id": "#didcomm-0",
                "type": "DIDCommMessaging",
                "serviceEndpoint": {
                    "uri": "http://localhost:5000",
                    "accept": ["didcomm/v2"],
                },
            }
        ],
        "keyAgreement": ["#key-1"],
    }

    return encode(_data)
