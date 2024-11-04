class Peer_DID:
    def __init__(self,did:str):
        self.did = did
    def __validate__(self):
        _splitted = self.did.split(":")
        if len(_splitted) == 4:
            if _splitted[0] == "did" and _splitted[1] == "peer":
                return self.did
            else:
                return None
        else:
            return None
    
    def __create_peer__(self):
        
        pass