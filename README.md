# Itslearning2google 
- Export weekplans from ItsLearning systems to a Google Calendar\n


# Installation
Log in to ItsLearning manually, and go to a page containing a week plan. Examine the url - three parameters are needed : 1. the name og the student as it is specified in the url, 2. The id of the student as specified in the url, 3. The base_url of the site.\n

To configure the aplication, fill in the configuration.xml document with the information and user credetials for ItsLearning, and a calander_id from google. This ID can be obtained from the options tab under a calendar in Google calender.\n
\n
The script requires autenthication with the Google API. On first run, a browser will open, and you will be propted to log in. A file named client_secret.json will be created. Modify the name of the file to client_secret_your-student-id.json, and place it in the root folder of the application. 



# Requirements

Run the requirements.txt with pip to install the required packages for python 2.7\n

Enable to google calendar API and get the client_secret.json file - see this tutorial https://developers.google.com/calendar/quickstart/python 
