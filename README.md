# fb-auth

## Install Mysql on your machine.

1) create the database, name whatever you want to name it. I have named it `fb_app`.
    Once the database is created. Configure the mysql settings in the environment file.
    Create the .env file(this is added in .gitignore) at the root of the project structure.

    Add the following values for variables.

    DB_USER="root"
    DB_PASS="12345678"
    DB_NAME="fb_app"
    DB_SERVICE="localhost"
    DB_PORT="3306"

    Rename these values according to your settings.


2) For Facebook Create the facebook app. and store the get the FB_ID and FB_ACCESS_TOKEN
    Set the values in the .env file
    FB_APP_ID=XXXXX
    FB_SECRET=XXXXXXXXXXX

### Steps to Run the Server.

    1) Create and activate VirtualEnv.
    2) RUN pip install -r requirements.txt
    3) RUN python manage.py migrate
    4) RUN python manage.py collectstatic --no-input
    5) RUN python manage.py runserver.
    6) HiT localhost:8000 on your browser machine.

To make sure that deauth callback works, we need https host. I use ngrok to get the
https corresponding host agains my localhost network. Once you delete the app from the facebook, it should trigger the
callback and deactivate the registered user.

