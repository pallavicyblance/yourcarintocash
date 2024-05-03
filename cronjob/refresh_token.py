import requests
import jwt
from Misc.functions import *
from module.acv import ACV

acv = ACV()
def refresh_token():
    refresh_token = acv.getjwttoken(acv_user()[0])

    refreshTokenurl = 'https://buy-api.gateway.staging.acvauctions.com/v2/login/refresh'
    data = {
        'refreshToken' : refresh_token[4]
    }
    response = requests.post(refreshTokenurl, json=data)
    try:
        jwtToken = response.json().get('jwt')

        print(jwtToken)

        acv.storeRefreshToken(jwtToken,acv_user()[0])

        # decoded_token = jwt.decode(jwtToken, options={"verify_signature": False}, algorithms=["HS256"])
        # expiration_timestamp = decoded_token.get('exp')
        # expiration_datetime = datetime.fromtimestamp(expiration_timestamp)
        # print("Token2 expiration datetime:", expiration_datetime)

        # refresh_token_bytes = refresh_token[4].encode('utf-8')
        # decoded_refresh_token = jwt.decode(refresh_token_bytes, options={"verify_signature": False}, algorithms=["HS256"])
        # refresh_token_exp_timestamp = decoded_refresh_token.get('exp')
        # refresh_token_exp_datetime = datetime.fromtimestamp(refresh_token_exp_timestamp)
        # print("Refresh token expiration datetime:", refresh_token_exp_datetime)

    except requests.exceptions.RequestException as e:
        print(response.text)
        return None 