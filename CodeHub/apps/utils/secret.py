import os, base64

def generate_secret(keylength:int):
    return base64.b64encode(os.urandom(keylength)).decode("ascii")