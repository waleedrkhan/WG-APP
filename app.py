from flask import Flask
from mailchimp_transactional.api_client import ApiClientError
import mailchimp_transactional as MailchimpTransactional

from flask_ngrok import run_with_ngrok


app = Flask(__name__)
# run_with_ngrok(app)

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
        response = client.webhooks.add({"url": "https://c0e1-111-119-187-8.in.ngrok.io/", "description": "My Example Webhook",
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


@app.route("/")
def mandrill_response():
    print("got a response from mandrill")
    return "<p>Response</p>"


@app.route("/send-mail")
def send_mail():
    try:
        response = mailchimp.messages.send({"message": message})
        print('API called successfully: {}'.format(response))
    except ApiClientError as error:
        print('An exception occurred: {}'.format(error.text))
        return "<p>Failed with error : {}</p>".format(error.text)
    return "<p>Success</p>"
# send_mail()

if __name__ == '__main__':
    app.run()
