# =============================================================================
# Created By  : Dustin Morris
# Created Date: Mon November 20 2023
# =============================================================================
# Interpreter: Python 3.12
# File Name: WSGI_Server.py
# =============================================================================
__course__ = 'CS499'
__author__ = 'Dustin Morris'
__version__ = '1.4'
__maintainer__ = 'Dustin Morris'
__username__ = 'MyUserAdmins2'
__password__ = '123456'
__email__ = 'Dustin.Morris1@snhu.edu'
__status__ = 'Production'
__description__ = 'File used to start wsgi server'
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

# Imports app object from Application.py module.
from Application import app
from Authentication import authenticate_user, logout_user, get_current_user

# Running Dash web server
if __name__ == "__main__":
    app.run_server()
