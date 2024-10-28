# Hexadecimal hash name format
import hashlib

def hex_url2path (url):
    result_hash = hashlib.md5(bytes(url, encoding='utf-8')).hexdigest()
    return result_hash
