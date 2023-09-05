# Place-for-dinner
My small app:
- to add cafes and restaurants to the list
- to select which place i shell visit today
- to log my visits to places
It will have api and frontend part
To start the application:
First add information to .env file (change name of exsmaple.env)
To run containers:
``` docker-compose up --build -d ```
If its a first run(for a postgre container) make migrations whith this command:
``` docker exec app_backend_1 python migration.py ```
