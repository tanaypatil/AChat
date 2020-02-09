# **ACHAT**

#### _**A ChatBot**_

ACHAT is a chat-bot web application with the following features:
1. A login/register system to sign in and use the bot.
2. Has the ability to accept text messages and replies with hardcoded string.
3. The webapp has an option to upload files which are in .pdf format.
4. It has a UI for listing the uploaded files.
5. It has a page where it accepts feedback/rating to the bot

_Technologies Used_:

**Django(Python web framework), HTML, CSS, jQuery, Bootstrap**

**Database - SQLite3**

**Python Version - 3.6.6**

Steps to run the project in development:
1. Install required python version.
2. Clone the project folder.
3. Setup a python virtual environment.
4. Activate the python virtual environment.
5. Install required packages from **_requirements.txt_** file using the command - 
<br>`pip install -r requirements.txt`
6. Navigate to the project folder. Run the command - <br>`python manage.py runserver`<br> to start the project on localhost.
7. Go to _127.0.0.1:8000_ on your browser.

<br>

**Production Environment:**<br>
Hosted on - **AWS EC2**<br>
Static & Media File Storage - **AWS S3**<br>
Web Server - **Apache2**