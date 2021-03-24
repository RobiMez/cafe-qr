import hashlib

def encode_uid(uid):
    encoded = hashlib.md5(uid.encode('utf-8'))
    return encoded.hexdigest()

