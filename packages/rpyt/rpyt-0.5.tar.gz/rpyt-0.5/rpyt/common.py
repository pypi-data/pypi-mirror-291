import hashlib
from typing import Any


def hash_object(obj: Any, length=8):
    # Convert the tuple to a string representation
    tuple_string = str(obj)

    # Create a SHA-256 hash of the string
    sha = hashlib.sha256(tuple_string.encode())

    # Convert the hash to a hexadecimal string and take the first 8 characters
    hash_hex = sha.hexdigest()[:length]

    return hash_hex
