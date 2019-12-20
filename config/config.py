import os
"""
to generate secret key you can os or secrets
os
import os
os.urandom(16).hex()

secrets
import secrets
secrets.token_hex(16)
"""


class Development():
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:re@127.0.0.1:5432/sales_demo'
    SECRET_KEY = os.urandom(16).hex()
    DEBUG = True
    SQLALCHEMY_ECHO = True
