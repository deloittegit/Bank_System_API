from flask_sqlalchemy import SQLAlchemy
import pandas as pd 
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, DateTime, Date
from sqlalchemy import func, desc, extract
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete
from flask_marshmallow import Marshmallow
import pythonlibrary
from pythonlibrary import myfunctions


engine = create_engine('sqlite:///Bank.db', echo = True)
Session = sessionmaker(bind = engine)
session = Session()
Base = declarative_base()

#Function to read the data
def read_csv(x):
    df = pd.read_csv(x)
    df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    df2 = df.dropna()
    df3 = df2.drop_duplicates()
    df3['LastUpdatedTime'] = pd.Timestamp('now')
    return df3

#Function to load the data 
def data_load(x):
    session.add_all(x)
    session.commit()

UserDetaildf = read_csv('UserDetails.csv')
class UserDetails(Base):
   __tablename__ = 'UserDetails'
   UserId = Column(String, primary_key=True)
   UserName = Column(String)
   Address = Column(String)
   Email = Column(String)
   LastUpdatedTime = Column(TIMESTAMP)

   def __init__(self, UserId, UserName, Address, Email, LastUpdatedTime):
    self.UserId = UserId
    self.UserName = UserName
    self.Address = Address
    self.Email = Email
    self.LastUpdatedTime = LastUpdatedTime

listofUserDetailsobjects = [(UserDetails(row.UserId, row.Username, row.Address, row.Email, row.LastUpdatedTime)) for index, row in UserDetaildf.iterrows()]

AccountDetailsdf = read_csv('UserAccountDetails.csv')   
class UserAccountDetails(Base):
    __tablename__ = 'UserAccountDetails'
    UserId = Column(String, ForeignKey('UserDetails.UserId'))
    AccountNumber = Column(Integer, primary_key=True)
    AccountBalance = Column(Integer)
    LastUpdatedTime = Column(TIMESTAMP)
    def __init__(self, UserId, AccountNumber, AccountBalance, LastUpdatedTime):
        self.UserId = UserId
        self.AccountNumber = AccountNumber
        self.AccountBalance = AccountBalance
        self.LastUpdatedTime = LastUpdatedTime
listofAccountDetailsobjects = [(UserAccountDetails(row.UserId, row.AccountNumber, row.AccountBalance, row.LastUpdatedTime)) for index, row in AccountDetailsdf.iterrows()]

df = pd.read_csv('UserTransactionsDetailsRe_Zero.csv')
df.insert(0, 'TransactionId', df.index + 1)
class UserTransactionDetails(Base):
    __tablename__= 'UserTransactionDetails'
    TransactionId = Column(Integer, primary_key = True)
    AccountNumber = Column(Integer, ForeignKey('UserAccountDetails.AccountNumber'))
    TransactionDate = Column(String)
    Description = Column(String)
    Withdrawal = Column(Integer)
    Deposit = Column(Integer)
    Balance = Column(Integer)
    def __init__(self, TransactionId, AccountNumber, TransactionDate, Description, Withdrawal, Deposit, Balance):
        self.TransactionId = TransactionId
        self.AccountNumber = AccountNumber
        self.TransactionDate = TransactionDate
        self.Description = Description
        self.Withdrawal = Withdrawal
        self.Deposit = Deposit
        self.Balance = Balance
listofTransactionDetailsobjects = [(UserTransactionDetails(row.TransactionId, row.AccountNumber, row.TransactionDate, row.Description, row.Withdrawl, row.Deposit, row.Balance)) for index, row in df.iterrows()]

listminimmumbalance = []
obj = session.query(UserAccountDetails.AccountBalance).filter(UserAccountDetails.AccountBalance < 800).all()
for i in range(len(obj)):
    listminimmumbalance.append('receiveremail123@gmail.com')

#Classes to make the SQLalchemy output json serializable using Marshmallow
ma = Marshmallow()
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

obj = myfunctions.readandparse_csv('UserDetails.csv')
print(obj)





