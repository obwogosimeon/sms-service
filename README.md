# SMS REST API


## Usage

### With docker mock database - for development

We the repository "farmer-db-docker-mock", which is integrated into this repository as git submodule
in the directory `/db`.

* initialize db submodule `git submodule init`
* update the db submodule to get the code: `git submodule update`
* `cp .env.docker.dev.flask.example .env.docker.dev.flask`
* run `docker-compose -f docker-compose.yml -f dc-add-mock-db.yml up` (add `-f dc-expose-ports.yml` as well, if you want to specify ports)
* run seeding, if the database volume was created fresh: `docker-compose exec sms_flask python /app/manage.py seed_database`


# Deprecated #


Test of a RESTful API with Flask and SQLAlchemy, based on  this [blog post](http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/). 
It was adapted to our needs and Flask-RESTPlus was replaced with the newer Flask-RESTX.


## Setup

### Create & Activate Virtual Environment

```
python3 -m venv env
source env/bin/activate
```

### Install Requirements
```
pip install -r requirements.txt
```

### Create .env File
The .env file holds environment dependant parameters and sensitive data that should not be stored
in git, like the database password. 

Copy the example file and fill the values:
```
cp .env.example .env
```


## Development

### Create database tables
```
python app.py db upgrade
```

### Seed database
Populate the database with data by executing the follow commands
```
chmod +x seeding_script.sh
./seeding_script.sh
```

### Africastalking sandbox setup
- Download ngrok [here](https://ngrok.com/download)
- Make the file executable by issuing command `sudo chmod +x file_name`
- Run the app by issuing `python manage.py runserver` if the app is not running already
- Create a tunnel to the app's local address using ngrok by issuing the command:
  - `./ngrok http 8000` then you will get a public address to use e.g. `https://dfeae46b.ngrok.io`
- Login to AfricasTalking [account](https://account.africastalking.com/)
- Get API key [here](https://account.africastalking.com/apps/sandbox/settings/key) and update your environment variable
- Create a [channel](https://account.africastalking.com/apps/sandbox/sms/shortcodes)
- Set callback for your Shortcode code. The callback is the public address generated by ngrok when you create a tunnel as described in instruction 4 above
- View your Short codes [here](https://account.africastalking.com/apps/sandbox/sms/shortcodes)
- Access the simulator [here](https://simulator.africastalking.com:1517/simulator) and send test SMS

### Run Test Flask Server on Localhost
```
python app.py runserver
```

The API is now available at `localhost:5000/api/v1/`.
When calling this URL in the web browser, an interactive swagger definition is rendered.

### Project Structure

This is the project structure for our Flask application:
```
├── api                         #
│   ├── v1                      #  One directory per major API version
│   │   ├── business.py         #
│   │   ├── endpoints           #  API namespaces and REST methods
│   │   │   ├── sms.py          #
│   │   │   └── ...             #
│   │   ├── parsers.py          #  Argument parsers
│   │   └── serializers.py      #  Output serializers
│   ├── restx.py                #  API bootstrap file
│   └── version.py              #  Variable with API version
├── app.py                      #  Application bootstrap file
├── database                    #
│   └── models.py               #  Definition of SQLAlchemy models
├── .env                        #  Environment dependant variables
├── logs                        #
│   └── log.log                 #  Application logging file
├── migrations                  #
│   └── versions                #  Database migration files
├── seeds                       #  Database Seeding scripts
│   ├── sms_seeder.py
│   └── ...           
└── settings.py                 #  Global app variables
```

The main entry and point is `app.py`, where the Flask app is initialized, together with the 
Flask-RESTX API defined in `api/restx.py` and a database connection. 
Here, the namespaces of the endpoints are loaded. 

*Namespaces* (e.g. [../api/v1/sms]()) are the logical bundle for HTTP requests to our API. 
Each namespace should be defined in one Python file in the `../endpoints/` folder. 
Here we define the GET, POST, PUT and DELETE operations for the HTTP calls.

The *serializers* in `serializers.py` define how the return values to an HTTP request should be structured.
Here we also document the serializers for the Swagger definition/page.

*Parsers* defined in `parsers.py` are used to parse and validate the input of an HTTP request.

All business logic, like creation and deletion of objects in the database, are defined in `business.py`.

The data models for the database are defined with SQLAlchemy under `database/models.py`.

The API version is tracked under `api/version.py`. 
All changes to the API should be backward compatible within the same major API version.
