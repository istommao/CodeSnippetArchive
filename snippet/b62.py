"""Python b62."""
import xxhash_cffi

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62_encode(dec):
    return ALPHABET[dec] if dec < 62 else base62_encode(dec // 62) + ALPHABET[dec % 62]


def get_short_url_code(url):
    hash_num = xxhash_cffi.xxh32_intdigest(url)
    code = base62_encode(hash_num)

    return code
