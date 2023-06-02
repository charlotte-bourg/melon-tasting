Install requirements.txt to run

MVP status:
- Completed minimum requirements of assignment 
- Log in:
    - No validation. Checks for existing user with given string (should be email) or creates one. Adds user_id to session. 
    - Flash message specifies whether user was created on this login
- Home page:
    - Link to existing reservations
    - Search for new reservation time slot using date (required in HTML) and start and end times (optional)
- Search results:
    - Returns to home page with descriptive flash message if user selects a day on which they already have a reservation
    - Otherwise displays date & selected time range at top (with user friendly descriptors for "start of day" to "end of day" if the user leaves the optional start and end time fields black on their search)
    - Displays buttons for each available reservation time (checks for conflicts with other users' reservations and does not display those times)
- Booking:
    - Re-checks availability of appointment in case of race condition (another logged in user had a search with similar parameters and selected / was able to book that time first), and returns home with instructions in flash message if that occurs
    - If still available, books appointment in database and returns home with details of booked appointment in flash message. Can now be viewed in existing reservations too

Stack:
- Flask, SQLAlchemy, Postgres, HTML, Jinja

Database structure:
- User table:
    - ID (unique, primary key)
    - email
- Reservation table:
    - ID (unique, primary key)
    - date
    - start_time 
    - user_id (foreign key)

- Allows one to many relationship between users and reservations

TODO (priority):
- Deploy
- Add tests (did some testing while developing, but need written tests)
- Add front end styling - particularly bad UX if time slots span a full day and you have a long list of buttons. To add some CSS and/or boostrap
- Add comments and docstrings
- Modularize for readability and maintainability 
- Handling for case where user enters start time after end time

TODO (enhancements):
- Password
- Improve time display (12 hour instead of 24 based on locale, option for time zones)
- Email validation with regex or similar