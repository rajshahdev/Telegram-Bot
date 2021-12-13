### Step 0 : Clone the Repository

- `git clone https://github.com/rajshahdev/bot-assignment.git`
- `cd bot-assignment`

### Step 1 : Install dependencies

`pip install -r requirements.txt`

### Step 2 : Run migrations

`python manage.py makemigration`
`python manage.py migrate`

### Step 3 : Download and use ngrok

`ngrok http 8000`

At this point, you will have to add the NGROK URLs to ALLOWED_HOSTS in `chatbot_tutorial/settings.py`.

### Step 4 : Start the local server

And start the server with

`python manage.py runserver`

### Step 5 : Talk to the BotFather and get and set your bot token

from Botfather(telegram) Copy the token and paste in `chatbot_tutorial/views.py`

### Step 6 : Set your webhook by sending a post request to the Telegram API

If you are on a system where you can run a curl command, run the following command in your terminal (Remember to replace ngrok_url and bot_token)

`curl -F “url=<ngrok_url>/ngrok_token/“ https://api.telegram.org/bot<bot_token>/setWebhook`

You should get a response that states that "webhook has been set"

### Step 7 : Talk to the bot

### Step 8: To View the users interacting with the bot and their total number of calls made
- Visit `localhost:8000/telegrambot`