# WG-APP

To run the project/app follow the following steps

1. create a virtualenv with python3.8
2. install the requirements in req.txt file
3. run the flask app in terminal/pycharm on port 5000
4. open terminal and run the following command as root user. this will expose our application to the mailchimp where we can add webhooks for this url: ssh -R 80:localhost:5000 nokey@localhost.run
5. once we have the tunnel in terminal up and running it will provide us a url at the bottom ending with *.lhrtunnel.link copy and replace this url in config file of the app in pathURL
6. once the app is up and running you can navigate to the tunnel link provided in pathURL of the config file
7. start the app by accessing the link pathURL/add-hook. this will add a webhook in mandrill and send out one email and the response will be displayed in the web browser


Please go through the conf.cfg file in the repo to make the following adjustments
1. add your api key
2. add the required pathURL
3. set the from email as per your mailchimp account
