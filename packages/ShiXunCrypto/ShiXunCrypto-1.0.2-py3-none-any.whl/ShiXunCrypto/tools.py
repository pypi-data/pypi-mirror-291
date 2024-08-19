import hashlib


__all__ = [
    'SHA256'
]



def SHA256(data: str) -> str:
    if not isinstance(data, str):
        error_message = 'sha256沒有輸入正確的資料型態'
        raise TypeError(error_message)
    
    hash_obj = hashlib.sha256()
    hash_obj.update(data.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
    
    return hash_hex