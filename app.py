from flask import Flask
from mailchimp_transactional.api_client import ApiClientError
import mailchimp_transactional as MailchimpTransactional

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
api_key = 'YpncKdxeRDTYtugALhMJ-Q'

mailchimp = MailchimpTransactional.Client(api_key=api_key)
message = {
    "from_email": "manny@mailchimp.com",
    "subject": "Hello world",
    "text": "Welcome to Mailchimp Transactional!",
    "to": [
      {
        "email": "waleedrkhan90@gmail.com",
        "type": "to"
      }
    ]
}


def send_mail():
    try:
        response = mailchimp.messages.send({"message": message})
        print('API called successfully: {}'.format(response))
    except ApiClientError as error:
        print('An exception occurred: {}'.format(error.text))


send_mail()

if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
