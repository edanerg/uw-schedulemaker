## Progress info
Current features:
- Users can select a range of dates and times, which will show all available classes in that date range and time period.
- Users can view  all the courses in all faculties and see the course descriptions, and filter them based on subject or course code.
- Users can log in and add any courses that they have already taken.

Future addition:
- Students will be able to upload their schedule, and the web app will show all the classes that they can take in their schedule's free slots. (If possible, prerequisites and filter preferences will be taken into consideration)
- The Waterloo API will be used to get class info and populate the database.
- When filtering classes, we should not include any courses that the user has already taken.
- If a lecture is available, then the corresponding TUT or TST should also be considered.

## To test the app locally
The README.txt of the backend and frontend repo shows the instruction to run the app.

## Database Creation
The queries for creating tables are located in the file /backend/database/createtables.sql.
The backend app will execute that sql file which creates the tables for the SQL database.

## Database Population
Using Google Cloud Shell and MySQL, the commands in /backend/database/sql/sampledataset.sql are executed manually.

## How the Web app receives data from the SQL database
The backend grabs the data from SQL database in gcp (via sqlalchemy) and sends that data to the web app whenever the webapp executes a GET request to the backend API (on /courses route).

## Web App link
https://cs348-webapp10.appspot.com/
Note: currently this does not work because our free trial for GCP expired.

## Backend API link
https://cs348-database10.appspot.com/courses
Note: currently this does not work because our free trial for GCP expired.
