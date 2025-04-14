import uuid
from datetime import datetime, timedelta

def generate_reset_token():
    return str(uuid.uuid4())

def token_expiry(hours=1):
    return datetime.utcnow() + timedelta(hours=hours)
