


import time
import jwt

class JwtToken:

    # Called by outside function
    def get_token(self):
        return jwt.encode(self.get_payload(), "jwt secret", algorithm="HS256")

    def get_payload(self):
        return {'iss': "jwt issuer", 
                'scope': "jwt scope", 
                'aud': "jwt audience", 
                'domains': "jwt domains", 
                'name': "jwt name", 
                'iat': int(time.time()), 
                'exp': int(time.time()) + ("token expire time in minutes (int)" * 60000)}

# Example
jwtToken = JwtToken()
token = jwtToken.get_token()