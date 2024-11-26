

def singup_response(user):
    return {
        "message":"created",
         "data":{
                "id": user.id,
                "username": user.username,
                "phonenumber": user.phonenumber,
                "role":user.role
            }}
def login_response(access_token,refresh_token):
    return {
            "status": "success",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }