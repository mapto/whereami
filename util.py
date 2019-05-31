import re, hashlib
from urllib.parse import unquote

def normalize(address: str):
    return re.sub(r'\s+', ' ', unquote(address).upper())  # normalize address

def hash(address: str):
    return hashlib.md5(bytes(address, encoding="utf-8")).hexdigest()
