
# how to run locally

First clone this repo by using following command
````

git clone https://github.com/aminjamshidi/ChatBot_with_Reasoning.git

````
cd ChatBot_with_Reasoning

````
creat virtual environment

````
then set the .env file
````
GEMINI_API_KEY=AIzaSyBXGJZlGzaamvhTnYMPATizkkV_OflUAig
GOOGLE_API_KEY=AIzaSyBXGJZlGzaamvhTnYMPATizkkV_OflUAig
````
then install the requirements
````
pip install -r requirements.txt
````
then run the APIs
````
uvicorn API.main:app --reload --host 0.0.0.0 --port 8000

then run telegram bot
````
python TelBot.py
