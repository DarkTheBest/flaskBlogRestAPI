from passlib.hash import sha256_crypt


def hash_password(password: str):
    return sha256_crypt.hash(password)

