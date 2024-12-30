import pymongo, os
import secrets  # Import secrets for token generation
from config import DB_URL, DB_NAME

dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]
user_data = database['users']
token_data = database['tokens'] # New collection for tokens

# ... (Existing user management functions: present_user, add_user, full_userbase, del_user)
# ... (Existing shortener settings functions: set_shortener_settings, get_shortener_settings)

async def generate_token(user_id: int):
    token = secrets.token_urlsafe(32)  # Generate a cryptographically secure token
    token_data.insert_one({'user_id': user_id, 'token': token})
    return token

async def verify_token(token: str):
    token_doc = token_data.find_one({'token': token})
    if token_doc:
        return token_doc['user_id']
    return None

async def revoke_token(token: str):
    token_data.delete_one({'token': token})

async def get_user_tokens(user_id: int):
    tokens = []
    token_docs = token_data.find({'user_id': user_id})
    for doc in token_docs:
        tokens.append(doc['token'])
    return tokens
