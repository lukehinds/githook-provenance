#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib
import os.path
import sys
import webbrowser
import requests
import simplejson as json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from requests_oauthlib import OAuth2Session

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils

from securesystemslib.interface import import_ecdsa_privatekey_from_file
from securesystemslib.signer import SSlibSigner
import binascii


AUTH_TIMEOUT = 300

client_id = "sigstore"
client_secret = ""
redirect_uri = "http://localhost:3232"
auth_uri = "https://oauth2.sigstore.dev/auth/auth"
token_uri = "https://oauth2.sigstore.dev/auth/token"
userinfo_endpoint = "https://oauth2.sigstore.dev/auth/userinfo" 
scopes = (
    "openid",
    "email",
)

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Callback handler to log the details of received OAuth callbacks"""

    def do_GET(self):
        self.server.oauth_callbacks.append(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Auth details passed back to command line app")


class OAuthCallbackServer(HTTPServer):
    """Local HTTP server to handle OAuth authentication callbacks"""

    def __init__(self, server_address):
        self.oauth_callbacks = []
        HTTPServer.__init__(self, server_address, OAuthCallbackHandler)


def receive_oauth_callback(timeout):
    """Blocking call to wait for a single OAuth authentication callback"""
    server_address = ("", 3232)
    oauthd = OAuthCallbackServer(server_address)
    oauthd.timeout = timeout
    try:
        oauthd.handle_request()
    finally:
        oauthd.server_close()
    callback_path = oauthd.oauth_callbacks.pop()
    parsed_response = urlparse(callback_path)
    query_details = parse_qs(parsed_response.query)
    return query_details["code"][0], query_details["state"][0]


def register_fulcio_key():

    # this key can be made with in-toto-keygen -t ecdsa [filename]
    private_key = import_ecdsa_privatekey_from_file('testkey')
    public_key = private_key['keyval']['public']

    # this abstraction will allow us to sign with HSM's and whatnot.
    signer = SSlibSigner(private_key)
    
    #private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    #public_key = private_key.public_key()
    # serializing into PEM
    #rsa_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri, scope=scopes)
    authorization_url, state = oauth.authorization_url(auth_uri)
    wait_msg = "Waiting {0} seconds for browser-based authentication..."
    print(wait_msg.format(AUTH_TIMEOUT))
    webbrowser.open(authorization_url)
    # Technically a race condition, but should be faster than the OIDC
    # redirect flow even when the client has already been authenticated
    authorization_code, cb_state = receive_oauth_callback(AUTH_TIMEOUT)
    if cb_state != state:
        msg = "Callback state {0!r} didn't match request state {1!r}"
        raise RuntimeError(msg.format(cb_state, state))
    # client_token = oauth.fetch_token(
    #     token_uri, code=authorization_code, client_secret=client_secret
    # )
    session = oauth.fetch_token(
        token_uri, code=authorization_code, client_secret=client_secret
    )
    user_info = oauth.get(userinfo_endpoint).json()

    if not user_info["email_verified"]:
        print("User email must be verified")
        sys.exit(1)
    print(f"Retrieved user email: {user_info['email']}")

    # hash_object = hashlib.sha256(user_info['email'].encode())
    
    proof = signer.sign(user_info['email'].encode())
    proofb64 = base64.b64encode(binascii.unhexlify(proof.signature)).decode("utf8")

    payload = {"publicKey": {"content": public_key, "algorithm": "ecdsa"},"signedEmailAddress": proofb64}
    y = json.dumps(payload)
    print(y)
    
    headersAPI = {
            'Authorization': f'Bearer {session["id_token"]}',
            'Content-Type': 'application/json'
    }
    r = requests.post("https://fulcio.sigstore.dev/api/v1/signingCert", data=y,  headers=headersAPI)
    print(r.status_code)

    return private_key, payload

if __name__ == "__main__":
    register_fulcio_key()
