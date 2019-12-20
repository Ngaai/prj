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

class Production():
    SQLALCHEMY_DATABASE_URI = 'postgres://lqhmckjtescrdd:c5c24c71bf040dd26e768204c29971da8ee7534a60914bdc596b993ae5df777a@ec2-174-129-33-186.compute-1.amazonaws.com:5432/d2i1laq46b11tl'
    SECRET_KEY = os.urandom(16).hex()
    DEBUG = True
    SQLALCHEMY_ECHO = True
