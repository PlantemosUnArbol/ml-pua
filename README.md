### Start the a python virutal environment
#### Run python3 -m venv virtualenv
#### Active the environment with source virtualenv/bin/activate (for mac or linux)

### Install the libraries needed for the project
#### Run pip install -r requirenments.txt

### Start the project with
#### gunircorn app:app or
#### flask --app app run, for the first time, then only flask run

### Deploying the app
#### The easiest way is deploying the app with Caddy server and gunircorn
#### Once installed Caddy on the server, run caddy start inside the project folder
#### and gunicorn app:app &, the "&" option is to leave the gunicorn server runing when you exit the terminal
#### Make sure to configure the Caddyfile propperly

