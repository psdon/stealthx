from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5

hash = "SHA-256"


def new_keys(keysize):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private


def import_key(external_key):
    return RSA.importKey(external_key)


def get_public_key(priv_key):
    return priv_key.publickey()


def encrypt(message, pub_key):
    # RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)


def decrypt(cipher_text, priv_key):
    # RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(cipher_text)


def sign(message, priv_key, hash_alg="SHA-256"):
    global hash
    hash = hash_alg
    signer = PKCS1_v1_5.new(priv_key)
    if hash == "SHA-512":
        digest = SHA512.new()
    elif hash == "SHA-384":
        digest = SHA384.new()
    elif hash == "SHA-256":
        digest = SHA256.new()
    elif hash == "SHA-1":
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.sign(digest)


def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    if hash == "SHA-512":
        digest = SHA512.new()
    elif hash == "SHA-384":
        digest = SHA384.new()
    elif hash == "SHA-256":
        digest = SHA256.new()
    elif hash == "SHA-1":
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.verify(digest, signature)
