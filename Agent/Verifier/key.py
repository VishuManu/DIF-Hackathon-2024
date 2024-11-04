from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import os
import base58
import json
import base64


class Key:
    def __init__(self, location, loaded_private=None) -> None:
        self.location = location
        if not loaded_private:
            self.__private_key = ed25519.Ed25519PrivateKey.generate()
            self.public_key = self.__private_key.public_key()

            if os.path.exists(self.location):
                with open(os.path.join(self.location, "holder_key.json"), "w+") as F:
                    json.dump(
                        {
                            "id": self.hex_to_did_key(
                                self.get_pub()
                                .public_bytes(
                                    encoding=serialization.Encoding.Raw,
                                    format=serialization.PublicFormat.Raw,
                                )
                                .hex()
                            ),
                            "private_key": self.__private_key.private_bytes(
                                encoding=serialization.Encoding.Raw,
                                format=serialization.PrivateFormat.Raw,
                                encryption_algorithm=serialization.NoEncryption(),
                            ).hex(),
                        },
                        F,
                        indent=4,
                    )
                    F.close()
                    print("Key Saved")

        else:
            private_key_bytes = bytes.fromhex(loaded_private)
            self.__private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
                private_key_bytes
            )
            self.public_key = self.__private_key.public_key()

    def sign(self, message):
        print(self.__private_key.sign(message))
        print(self.public_key.public_bytes(
                                    encoding=serialization.Encoding.Raw,
                                    format=serialization.PublicFormat.Raw,
                                )
                                .hex())
        return self.__private_key.sign(message)

    def __get_jwk_OKP_pub__(self):
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
        )
        x_b64url = (
            base64.urlsafe_b64encode(public_key_bytes).rstrip(b"=").decode("utf-8")
        )
        return x_b64url


    @staticmethod
    def load_ed25519_public_key_from_OKP_jwk(jwk):
        x_b64url = jwk
        padded_x = x_b64url + "=="
        x_bytes = base64.urlsafe_b64decode(padded_x)
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(x_bytes)
        print(public_key .public_bytes(
                                    encoding=serialization.Encoding.Raw,
                                    format=serialization.PublicFormat.Raw,
                                )
                                .hex())
        return public_key


    def get_pub(self):
        return self.public_key

    def verify(self, signature, message):
        try:
            self.public_key.verify(signature, message)
            return True
        except Exception:
            return False





