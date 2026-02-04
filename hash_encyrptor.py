import hashlib

def hash(value):

    hashed_value = hashlib.md5(value.encode()).hexdigest()

    return hashed_value