import json
import os
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# *** IMPORTANT ***
# This variable is for development and testing only. Remove in production
# For development, set to False for easy testing of endpoint function
# and True to test role-based user access
#auth_master = not (int(os.environ.get('CAPSTONE_RBAC_SKIP')) == 1)

auth_master = True

AUTH0_DOMAIN = 'fsnd-djh.au.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'


# AuthError Exception
# A standardized way to communicate auth failure modes
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Retrieve the authentication header from the request
def get_token_auth_header():
    if len(request.headers) == 0:
        raise AuthError({
            'code': 'missing_header',
            'description': 'Request lacks headers.'
        }, 401)
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'missing_header',
            'description': 'Request does not contain authorization header'
        }, 401)
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        raise AuthError({
            'code': 'malformed_header',
            'description':
                'Authorization header does not contain the expected 2 parts'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'malformed_header',
            'description': 'Authorization header does not have a bearer marker'
        }, 401)

    return header_parts[1]


# Check that the payload matches the desired permission
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_permission',
            'description': 'No permissions found in authentication token'
        }, 400)
    if permission not in payload['permissions']:
        print(permission)
        print(payload['permissions'])
        raise AuthError({
            'code': 'invalid_permission',
            'description':
                'Authentication token did not contain the required permissions'
        }, 403)
    return True


# Verify that the JWT matches the public key
# and then decode it to extract the payload
def verify_decode_jwt(token):
    # Request public key from Auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # Extract the header from the JWT - we need to verify it
    unverified_header = jwt.get_unverified_header(token)

    # Choose the public key that matches the JWT
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Use the public key to verify that the JWT is valid
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        # Handle possible errors caused by invalid keys
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description':
                    'Incorrect claims. Please check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    # If we couldn't find a matching key, also raise an exception
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


# Decorator for ensuring that a function can only be called
# if the user has specific permissions
# Wrapped function should have variable "request" in its scope
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if auth_master:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                return f(*args, **kwargs)
            else:
                return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
