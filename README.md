## Progress info
Currently, the Web App only shows all the courses stored in the 'Courses' table.

Future addition:
- Users will be able to select a range of date, which will show all available classes in that date range
- Students will be able to upload their schedule, and the web app will show all the classes that they can take in their schedule's free slots. (Prerequisites and filter preferences will be taken into consideration)
- Students will be able to view all the courses in all faculties and see the course descriptions, along with the class times + instructors teaching the course + class sizes (users won't need to go to Undergrad calender to view the course descriptions and then go to quest to view the class times).
- The Waterloo API will be used to get class info and populate the database.

## To test the app locally
The README.txt of the backend and frontend repo shows the instruction to run the app.

## Database Creation
The queries for creating tables are located in the file /backend/database/createtables.sql
The backend app will execute that sql file which creates the tables for the SQL database.

## Database Population
Using Google Cloud Shell and MySQL, the commands in /backend/database/sql/sampledataset.sql are executed manually.

## How the Web app receives data from the SQL database
The backend grabs the data from SQL database in gcp (via sqlalchemy) and sends that data to the web app whenever the webapp executes a GET request to the backend API (on /courses route).

## Web App link
https://cs348-webapp10.appspot.com/

## Backend API link
https://cs348-database10.appspot.com/courses
