from jwt import encode, decode

def create_token(data: dict):
    token: str = encode(payload = data, key='my_sql_key', algorithm='HS256')
    
    return token

def validate_token(token: str):
    
    data = decode(token, key="my_secret_key", algorithms=["HS256"])
    
    return data
    