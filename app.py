from flask import Flask, jsonify
import logging
from flask_mail import Mail, Message
from methods import *
app = Flask(__name__)

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

if __name__=="__main__":
    app.run(debug='True', port = 8000)