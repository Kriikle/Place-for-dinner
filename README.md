# Place-for-dinner
My small app:
- to add cafes and restaurants to the list
- to select which place i shell visit today
- to log my visits to places
<br />It will have api and frontend part
## To start the application:
<br />First add information to .env file (change name of exsmaple.env)<br />
To run containers:<br />
``` docker-compose up --build -d ```<br />
<br />If its a first run(for a postgre container) make migrations whith this command:<br />
``` docker exec app_backend_1 python migration.py ```<br />
