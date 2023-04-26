from flask import Flask, jsonify, url_for, redirect
from flask import session as ses
import logging
from flask_mail import Mail, Message
from methods import *
from authlib.integrations.flask_client import OAuth
import os
#from auth_decorator import login_required
app = Flask(__name__)

app.config['SERVER_NAME'] = '127.0.0.1:8000'
app.config['SECRET_KEY'] = "Your_secret_string"
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="932918296221-l7ar071dfm0mqjgqtnccuj6mejibce04.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration',
)


#changing the level of the logging to debug
logging.basicConfig(level=logging.DEBUG)

#calling the mail object
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sendersmail123@gmail.com'
app.config['MAIL_PASSWORD'] = 'nyaedlzboatehstz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
#@login_required
def hello_world():
    email = dict(ses).get('email', None)
    return f'Hello, you are logged in as {email}!'

@app.route("/userDetailsDataLoad", methods=['POST'])
def user_data_load():
    k = data_load(listofUserDetailsobjects)
    app.logger.info('Dataload request')
    return "Data loaded successfully"

@app.route("/AccountDetailsDataLoad", methods=['POST'])
def account_data_load():
    l = data_load(listofAccountDetailsobjects)
    app.logger.info('Dataload request')
    return "Data loaded successfully"

@app.route("/TransactionDetailsDataLoad", methods=['POST'])
def transaction_data_load():
    m = data_load(listofTransactionDetailsobjects)
    app.logger.info('Dataload request')
    return "Data loaded successfully"

@app.route("/readUserDetails/<numberofrecords>", methods=['GET'])
def read_user_details(numberofrecords):
    obj = session.query(UserDetails).limit(numberofrecords).all()
    output = users_schema.dump(obj)
    app.logger.info('Requested data from the database')
    return output

@app.route("/readUserAccountDetails/<numberofrecords>", methods=['GET'])
def read_user_account_details(numberofrecords):
    obj = session.query(UserAccountDetails).limit(numberofrecords).all()
    output = users_account_schema.dump(obj)
    app.logger.info('Requested data from the database')
    return output

@app.route("/readTransactionDetails/<numberofrecords>", methods=['GET'])
def read_user_transaction_details(numberofrecords):
    obj = session.query(UserTransactionDetails).limit(numberofrecords).all()
    output = users_transaction_schema.dump(obj)
    app.logger.info('Requested data from the database')
    return output

@app.route("/users/accountBalanceLessthan800", methods = ['GET'])
def balance_less_than_800():
    obj = session.query(UserAccountDetails).filter(UserAccountDetails.AccountBalance < 800).all()
    output = users_account_schema.dump(obj)
    app.logger.info('Requested data from the database')
    return output

@app.route("/users/<UserId>", methods = ['GET'])
def balance_inquiry(UserId):
    obj = session.query(UserAccountDetails.AccountBalance).filter(UserAccountDetails.UserId == UserId).all()
    output = users_account_schema.dump(obj)
    app.logger.info('Requested data from the database')
    return output

@app.route("/users/name/<x>", methods = ['GET'])
def user_func_display(x):
    obj = session.query(UserDetails).filter(UserDetails.UserName.like('%' + x + '%')).all()
    output = users_schema.dump(obj)
    app.logger.info('Requested data from the database')
    return output

@app.route("/users/topTenTransactionsUsersInMonth/<x>", methods = ['GET'])
def user_top10_tran(x):
    obj = session.query(UserTransactionDetails.AccountNumber, func.count(UserTransactionDetails.AccountNumber)).filter(UserTransactionDetails.TransactionDate.like('%' + x + '-' + '%')).group_by(UserTransactionDetails.AccountNumber).order_by(func.count(UserTransactionDetails.AccountNumber).desc()).limit(10).all()
    output = users_transaction_schema.dump(obj)
    app.logger.info('Requested data from the database')
    return output

@app.route("/sendEmailtoUsersWithBalanceLessThanMinimum", methods = ['POST'])
def mail_sender():
    msg = Message('Hello', sender ='sendersmail123@gmail.com', recipients = listminimmumbalance)
    msg.body = 'You have received the email because your account does not fulfill the minimum requirement.'
    mail.send(msg)
    return 'Sent'

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    #user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    ses['email'] = user_info['email']
    #session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')

if __name__=="__main__":
    app.run(debug='True', port = 8000)