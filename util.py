import re
from urllib.parse import unquote

def normalize(address: str):
    return re.sub(r'\s+', ' ', unquote(address).upper())  # normalize address
