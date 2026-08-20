# coding=utf-8
"""
    @project: Crafter.ai
    @Author：Tiger
    @file： rsa_util.py
    @date：2023/11/3 11:13
    @desc:
"""
import base64
import threading

from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey import RSA
from django.core import cache
from django.db.models import QuerySet

from common.constants.cache_version import Cache_Version
from local_model.models.system_setting import SystemSetting, SettingType

lock = threading.Lock()
rsa_cache = cache.cache
cache_key = "rsa_key"
# Encrypted KeysPassword
secret_code = "mac_kb_password"


def generate():
    """
    generate Private key pair
    :return:{key:'public key',value:'private key'}
    """
    # generateonepieces 2048 bitKeys
    key = RSA.generate(2048)

    # getprivate key
    encrypted_key = key.export_key(passphrase=secret_code, pkcs=8,
                                   protection="scryptAndAES128-CBC")
    return {'key': key.publickey().export_key(), 'value': encrypted_key}


def get_key_pair():
    rsa_value = rsa_cache.get(cache_key)
    if rsa_value is None:
        with lock:
            rsa_value = rsa_cache.get(cache_key)
            if rsa_value is not None:
                return rsa_value
            rsa_value = get_key_pair_by_sql()
            version, get_key = Cache_Version.SYSTEM.value
            rsa_cache.set(get_key(key='rsa_key'), rsa_value, timeout=None, version=version)
    return rsa_value


def get_key_pair_by_sql():
    system_setting = QuerySet(SystemSetting).filter(type=SettingType.RSA.value).first()
    if system_setting is None:
        kv = generate()
        system_setting = SystemSetting(type=SettingType.RSA.value,
                                       meta={'key': kv.get('key').decode(), 'value': kv.get('value').decode()})
        system_setting.save()
    return system_setting.meta


def encrypt(msg, public_key: str | None = None):
    """
    encryption
    :param msg:        encryptionNumberAccording to
    :param public_key: public key
    :return: encryptedNumberAccording to
    """
    if public_key is None:
        public_key = get_key_pair().get('key')
    cipher = PKCS1_cipher.new(RSA.importKey(public_key))
    encrypt_msg = cipher.encrypt(msg.encode("utf-8"))
    return base64.b64encode(encrypt_msg).decode()


def decrypt(msg, pri_key: str | None = None):
    """
    Decrypt
    :param msg: Need to decryptNumberAccording to
    :param pri_key: private key
    :return: After decryptionNumberAccording to
    """
    if pri_key is None:
        pri_key = get_key_pair().get('value')
    cipher = PKCS1_cipher.new(RSA.importKey(pri_key, passphrase=secret_code))
    decrypt_data = cipher.decrypt(base64.b64decode(msg), 0)
    return decrypt_data.decode("utf-8")


def rsa_long_encrypt(message, public_key: str | None = None, length=200):
    """
    Ultra-long text encryption

    :param message:         The character string that needs to be encrypted
    :param public_key   public key
    :param length:      1024bitcertificate for100， 2048bitcertificate for 200
    :return: encryptedNumberAccording to
    """
    # Read public key
    if public_key is None:
        public_key = get_key_pair().get('key')
    cipher = PKCS1_cipher.new(RSA.importKey(extern_key=public_key,
                                            passphrase=secret_code))
    # Processing：Plaintext is too long. segmentationencryption
    if len(message) <= length:
        # codedNumberAccording toEncrypt and encode via base64
        result = base64.b64encode(cipher.encrypt(message.encode('utf-8')))
    else:
        rsa_text = []
        # After encodingNumberAccording toSlice, reason: encryption length cannot be too long
        for i in range(0, len(message), length):
            cont = message[i:i + length]
            # After slicingNumberAccording toEncrypt and add Newarrivetext behind
            rsa_text.append(cipher.encrypt(cont.encode('utf-8')))
        # Splicing after encryption
        cipher_text = b''.join(rsa_text)
        # base64Encode
        result = base64.b64encode(cipher_text)
    return result.decode()


def rsa_long_decrypt(message, pri_key: str | None = None, length=256):
    """
    Decrypt very long text, not encrypted by default
    :param  message:    Need to decryptNumberAccording to
    :param  pri_key:    secret key
    :param  length :     1024bitThe certificate uses 128, and the 2048bit certificate uses 256 bits.
    :return: decryptedNumberAccording to
    """
    if pri_key is None:
        pri_key = get_key_pair().get('value')
    cipher = PKCS1_cipher.new(RSA.importKey(pri_key, passphrase=secret_code))
    base64_de = base64.b64decode(message)
    res = []
    for i in range(0, len(base64_de), length):
        res.append(cipher.decrypt(base64_de[i:i + length], 0))
    return b"".join(res).decode()
