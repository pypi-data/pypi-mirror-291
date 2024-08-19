# DualRegev
from DualRegev.Cipher.Crypto import LBDRKey, LBDRCrypt
from DualRegev.Config import config
from DualRegev.IO import Converter
# AES
from AdvancedEncryptionStandard.Cipher.Crypto import AESCrypto, AESKey
# python
import hashlib


class DualAES():
    """
    此class定義DualRegev與AES綜合加密法，
    方法為：DualRegev加密AES金鑰、AES加密文件。
    """
    def __init__(self, pk: bytes = None, sk: bytes = None) -> None:
        self.pk = pk        # .pem格式的DualRegev公鑰
        self.__sk = sk      # .pem格式的DualRegev私鑰
    
    @property
    def sk(self) -> None | bytes:
        return self.__sk


    def key_generate(self) -> tuple[bytes, bytes]:
        # 生成金鑰
        key_pair = LBDRKey.generate_key()
        
        # 取出公私鑰
        pk = key_pair.extract_key()
        sk = key_pair.extract_private_key()
        
        self.pk = pk
        self.__sk = sk
        return (pk, sk)


    def encrypt(self, data: str) -> bytes:
        # 沒有公鑰不能加密
        if self.pk == None:
            error_message = 'Without public key in objects.'
            raise ValueError(error_message)
        
        # 生成AES key
        AES_key_obj = AESKey.generate_key(256)
        AES_key = AES_key_obj.extract_key()
        
        # 用AES key把data加密
        AES_obj = AESCrypto()
        AES_obj.import_key(AES_key)
        enc_data = AES_obj.encrypt(data.encode('utf-8'))
        
        # 用DualRegev把AES_key加密
        DR_obj = LBDRCrypt()
        DR_obj.import_key(self.pk)
        enc_key = DR_obj.encrypt(AES_obj.key)
        
        return enc_key + b'|' + enc_data
    
    
    def decrypt(self, cipher_text: bytes) -> str:
        # 沒有私鑰不能解密
        if self.__sk == None:
            error_message = 'Without private key in objects.'
            raise ValueError(error_message)
        
        enc_key, enc_data = cipher_text.split(b'|')
        
        # 用DualRegev把AES_key解密
        DR_obj = LBDRCrypt()
        DR_obj.import_key(self.sk)
        key = DR_obj.decrypt(enc_key)

        # 用AES key把data解密
        AES_obj = AESCrypto()
        AES_obj.key = key
        AES_obj.gen_round_key()
        data = AES_obj.decrypt(enc_data)

        return data.decode()
    

    def import_key(self, key: bytes) -> None:
        _data = key.split(b'\n')
        if _data[0] == b'-----BEGIN DUAL REGEV PUBLIC KEY-----':
            self.pk = key
        elif _data[0] == b'-----BEGIN DUAL REGEV PRIVATE KEY-----':
            self.__sk = key
        else:
            error_message = 'Invalid key input.'
            raise ValueError(error_message)