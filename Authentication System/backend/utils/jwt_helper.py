from flask_jwt_extended import create_access_token, create_refresh_token

def generate_tokens(identity):
    access = create_access_token(identity = str(identity))
    refresh = create_refresh_token(identity = str(identity))
    return {"access": access, "refresh": refresh}



