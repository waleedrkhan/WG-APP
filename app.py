from flask import Flask, request, render_template
from mailchimp_transactional.api_client import ApiClientError
import mailchimp_transactional as MailchimpTransactional
import json
from flask_caching import Cache
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import redirect
import configparser

parser = configparser.ConfigParser()
parser.read("conf.cfg")

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
socketio = SocketIO(app)

api_key = parser.get('app-cfg', 'apiKey')
mailchimp = MailchimpTransactional.Client(api_key=api_key)
message = {
    "from_email": parser.get('app-cfg', 'fromEmail'),
    "subject": parser.get('app-cfg', 'subject'),
    "text": "These mails are specially for interview application.",
    "to": [
        {
            "email": parser.get('app-cfg', 'toEmail'),
            "type": "to"
        }
    ]
}


@app.route("/add-hook")
def add_webhook():
    try:
        client = MailchimpTransactional.Client(api_key=api_key)
        response = client.webhooks.add(
            {"url": parser.get('app-cfg', 'pathURL'), "description": "My Example Webhook",
             "events": [
                 "send",
                 "open",
                 "click",
                 "hard_bounce",
                 "spam",
                 "reject"
             ]})
        print(response)
        send_mail()
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return "<p>Failed to add hook: {}</p>".format(error.text)
    return "<p>Hook added successfully and email sent</p>"


@app.route("/", methods=['POST'])
@socketio.on('my_event')
def mandrill_response():
    try:
        data = json.loads(request.form['mandrill_events'])[0]
        cache.set(data.get("_id"), data)
        socketio.emit('my_event', data)
        return redirect('index.html', data=data)
    except Exception as e:
        pass
    return "<p>clean</p>"


# @app.route("/send-mail")
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
