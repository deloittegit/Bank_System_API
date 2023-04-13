from flask import Flask, jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pandas as pd 
from methods import *
import json

app = Flask(__name__)

ma = Marshmallow(app)
class UserDetailsSchema(ma.Schema):
    class Meta:
        fields = ('UserId', 'UserName', 'Address', 'Email', 'LastUpdatedTime')
user_schema = UserDetailsSchema()
users_schema = UserDetailsSchema(many=True)

class UserAccountDetailsSchema(ma.Schema):
    class Meta:
        fields = ('UserId', 'AccountNumber', 'AccountBalance', 'LastUpdatedTime')
user_account_schema = UserAccountDetailsSchema()
users_account_schema = UserAccountDetailsSchema(many=True)

class UserTransactionDetailsSchema(ma.Schema):
    class Meta:
        fields = ('TransactionId', 'AccountNumber', 'TransactionDate', 'Description', 'Withdrawal', 'Deposit', 'Balance')
user_transaction_schema = UserTransactionDetailsSchema()
users_transaction_schema = UserTransactionDetailsSchema(many=True)

@app.route("/userDetailsDataLoad", methods=['POST'])
def user_data_load():
    k = data_load(listofUserDetailsobjects)
    return "Data loaded successfully"


@app.route("/AccountDetailsDataLoad", methods=['POST'])
def account_data_load():
    l = data_load(listofAccountDetailsobjects)
    return "Data loaded successfully"


@app.route("/TransactionDetailsDataLoad", methods=['POST'])
def transaction_data_load():
    m = data_load(listofTransactionDetailsobjects)
    return "Data loaded successfully"

@app.route("/readUserDetails/<numberofrecords>", methods=['GET'])
def read_user_details(numberofrecords):
    obj = session.query(UserDetails).limit(numberofrecords).all()
    output = users_schema.dump(obj)
    return output

@app.route("/readUserAccountDetails/<numberofrecords>", methods=['GET'])
def read_user_account_details(numberofrecords):
    obj = session.query(UserAccountDetails).limit(numberofrecords).all()
    output = users_account_schema.dump(obj)
    return output

@app.route("/readTransactionDetails/<numberofrecords>", methods=['GET'])
def read_user_transaction_details(numberofrecords):
    obj = session.query(UserTransactionDetails).limit(numberofrecords).all()
    output = users_transaction_schema.dump(obj)
    return output

@app.route("/users/accountBalanceLessthan800", methods = ['GET'])
def balance_less_than_800():
    obj = session.query(UserAccountDetails).filter(UserAccountDetails.AccountBalance < 800).all()
    output = users_account_schema.dump(obj)
    return output

@app.route("/users/<UserId>", methods = ['GET'])
def balance_inquiry(UserId):
    obj = session.query(UserAccountDetails.AccountBalance).filter(UserAccountDetails.UserId == UserId).all()
    output = users_account_schema.dump(obj)
    return output

@app.route("/users/name/<x>", methods = ['GET'])
def user_func_display(x):
    obj = session.query(UserDetails).filter(UserDetails.UserName.like('%' + x + '%')).all()
    output = users_schema.dump(obj)
    return output

if __name__=="__main__":
    app.run(debug='True', port = 8000)