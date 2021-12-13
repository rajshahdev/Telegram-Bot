from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.db.models import F
from telegrambot.models import Call, User

def get_message_from_request(request):
    received_message = {}
    decoded_request = json.loads(request.body.decode('utf-8'))
    print(decoded_request)
    if 'message' in decoded_request:
        received_message = decoded_request['message']
        received_message['chat_id'] = received_message['from']['id'] # simply for easier reference
        received_message['first_name'] = received_message['from']['first_name']
        received_message['username'] = received_message['from']['username']
    print(received_message)
    return received_message


def insert_call(name):
    all_calls = Call.objects.all().filter(button_name=name)

    if all_calls.exists():
        all_calls.update(count=F("count") + 1)
    else:
        call = Call(button_name=name,count=1)
        call.save()


def insert_user(username, firstname):
    get_user = User.objects.all().filter(user_name=username)
    if get_user.exists():
        get_user.update(calls=F("calls") + 1)
    else:
        user = User(user_name=username, first_name=firstname, calls=1)
        user.save()



def send_messages(message, token):
    # Ideally process message in some way. For now, let's just respond

    jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""THis is fun""",
                    """THis isn't fun"""]
    }

    reply_markup={"keyboard":[["stupid","fat","dumb"]],"one_time_keyboard":True}
    default_message = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."


    post_message_url = "https://api.telegram.org/bot{0}/sendMessage".format(token)
    chat_id = message['chat_id']
    button_reply_data = {'chat_id': chat_id, 'text': default_message, 'reply_markup': json.dumps(reply_markup)}

    result_message = {}         # the response needs to contain just a chat_id and text field for  telegram to accept it
    result_message['chat_id'] = chat_id
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])

    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])

    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])

    else:
        requests.post(post_message_url, data=button_reply_data)

    response_msg = json.dumps(result_message)
    status = requests.post(post_message_url, headers={
        "Content-Type": "application/json"}, data=response_msg)
    insert_user(message['username'], message['first_name'])

    if (jokes.get(message['text'])):
        insert_call(message['text'])


class TelegramBotView(generic.View):

    # csrf_exempt is necessary because the request comes from the Telegram server.
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    # Post function to handle messages in whatever format they come
    def post(self, request, *args, **kwargs):
        TELEGRAM_TOKEN = 'TOKEN'
        start_message = get_message_from_request(request)
        send_messages(start_message, TELEGRAM_TOKEN)

        return HttpResponse()
