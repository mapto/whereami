import re
from urllib.parse import unquote

def normalise(address: str):
    return re.sub(r'\s+', ' ', unquote(address).upper())  # normalise address
