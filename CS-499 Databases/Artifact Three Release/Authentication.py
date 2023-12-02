# =============================================================================
# Created By  : Dustin Morris
# Created Date: Mon November 20 2023
# =============================================================================
# Interpreter: Python 3.12
# File Name: Authentication.py
# =============================================================================
__course__ = 'CS499'
__author__ = 'Dustin Morris'
__version__ = '1.4'
__maintainer__ = 'Dustin Morris'
__username__ = 'MyUserAdmins2'
__password__ = '123456'
__email__ = 'Dustin.Morris1@snhu.edu'
__status__ = 'Production'
__description__ = 'Authentication control for user login and logout'
# =============================================================================
print('# ' + '=' * 78)
print('Author: ' + __author__)
print('Version: ' + __version__)
print('Maintainer: ' + __maintainer__)
print('Email: ' + __email__)
print('Status: ' + __status__)
print('Course: ' + __course__)
print('Username: ' + __username__)
print('Password: ' + __password__)
print('Description: ' + __description__)
print('# ' + '=' * 78)


from passlib.hash import pbkdf2_sha256
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://myUserAdmins2:123456@localhost:27017/AAC?authSource=AAC')
db = client['AAC']  # Name of the database
collection_users = db['users']  # Collection registered users are stored in.

def authenticate_user(username, password):
    # Find the user in the 'users' collection by username
    user = collection_users.find_one({'username': username})

    if user and pbkdf2_sha256.verify(password, user['password']):
        return True
    else:
        return False

def logout_user():
    global current_user
    current_user = None

current_user = None  # Global variable to store the current user

def authenticate_user(username, password):
    global current_user
    # Searches 'users' collection for username
    user = collection_users.find_one({'username': username})

    if user and pbkdf2_sha256.verify(password, user['password']):
        current_user = username  # Sets the current user
        return True
    else:
        current_user = None  # Resets the current user on failed authentication
        return False

def get_current_user():
    return current_user