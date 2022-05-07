from flask import Flask, request, render_template
from mailchimp_transactional.api_client import ApiClientError
import mailchimp_transactional as MailchimpTransactional
import json
from flask_caching import Cache
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
socketio = SocketIO(app)

api_key = 'YpncKdxeRDTYtugALhMJ-Q'
mailchimp = MailchimpTransactional.Client(api_key=api_key)
message = {
    "from_email": "no-reply-waleed@mailchimp.com",
    "subject": "Test App Mails",
    "text": "These mails are specially for interview application.",
    "to": [
        {
            "email": "waleedrkhan90@gmail.com",
            "type": "to"
        }
    ]
}


@app.route("/add-hook")
def add_webhook():
    try:
        client = MailchimpTransactional.Client(api_key=api_key)
        response = client.webhooks.add(
            {"url": "https://7c5328ba6f6597.lhrtunnel.link", "description": "My Example Webhook",
             "events": [
                 "send",
                 "open",
                 "click",
                 "hard_bounce",
                 "spam",
                 "reject"
             ]})
        print(response)
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return "<p>Failed to add hook: {}</p>".format(error.text)
    return "<p>Hook added successfully</p>"


@app.route("/", methods=['POST'])
@socketio.on('message')
def mandrill_response():
    print("got a response from mandrill")
    try:
        data = json.loads(request.form['mandrill_events'])[0]
        cache.set(data.get("_id"), data)
        socketio.emit('my_socket_event', data)
    except Exception as e:
        pass
    return render_template('index.html')


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    print("is data here now")


@app.route("/send-mail")
def send_mail():
    try:
        response = mailchimp.messages.send({"message": message})
        print('API called successfully: {}'.format(response))
    except ApiClientError as error:
        print('An exception occurred: {}'.format(error.text))
        return "<p>Failed with error : {}</p>".format(error.text)
    return "<p>Success</p>"


if __name__ == '__main__':
    app.run()
