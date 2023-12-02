~~~~Simplified instructions to run application~~~~

- Load the current included files into your IDE

- Install the required libraries with the included requirements.txt ($ pip install -r requirements.txt)

- Change the address to your mongodb making sure the port, username, password is correct in 'Application.py', 'AnimalClass.py', 'Authentication.py'.

- Run Application.py

- Run the follow command in your IDE terminal `waitress-serve --host=0.0.0.0 --port=8050 WSGI_Server:app` this will allow you to connect to the application on a machine within the same network.

- Click "Open Register" and give yourself a username and password.  

- Then click "Open Login" to be given access to adding new animal data to the database.