#!/usr/bin/python
import json
from bson import json_util
from pymongo.collection import ReturnDocument
import bottle
from bottle import route, run, get, request, abort, post, put, delete
import datetime
from pymongo import MongoClient
import pymongo.errors

# setup URI paths for REST service
@post('/stocks/api/v1.0/createStock/<newticker>')
def create_document(newticker):
  new_doc = request.json
  
  connection = MongoClient('localhost', 27017)
  db = connection['market']
  collection = db['stocks']

  try:
    new_doc["Ticker"] = newticker
    result = collection.save(new_doc)
    return "Created stock for ticker symbol " + newticker + "\n"

  except:
    return "Unable to add ticker\n"

@get('/stocks/api/v1.0/getStock/<ticker>')
def get_stock(ticker):
  connection = MongoClient('localhost', 27017)
  db = connection['market']
  collection = db['stocks']

  try:
    result = collection.find_one({"Ticker" : ticker}) 
    return json.loads(json.dumps(result, indent=4, default=json_util.default))
  
  except pymongo.errors.OperationFailure as oe:
    return oe 


@put('/stocks/api/v1.0/updateStock/<ticker>')
def update_stock(ticker):
  updates = request.json 
  connection = MongoClient('localhost', 27017)
  db = connection['market']
  collection = db['stocks']

  try:
    updated_doc = collection.find_one_and_update({"Ticker" : ticker}, {"$set" : updates}, return_document=ReturnDocument.AFTER)
    return json.loads(json.dumps(updated_doc, indent=4, default=json_util.default))

  except pymongo.errors.OperationFailure as oe:
    return oe 


@delete('/stocks/api/v1.0/deleteStock/<ticker>')
def delete_stock(ticker):

  connection = MongoClient('localhost', 27017)
  db = connection['market']
  collection = db['stocks']

  try:
    result = collection.delete_one({"Ticker" : ticker})
    return "Deleted stock symbol " + ticker + "\n" 

  except pymongo.errors.OperationFailure as oe:
    return oe 


@post('/stocks/api/v1.0/stockReport')
def get_report():
  list = request.json['list']
  
  connection = MongoClient('localhost', 27017)
  db = connection['market']
  collection = db['stocks']

  result = {}    # empty dictionary

  try:
    for ticker in list:
        doc = collection.find_one({"Ticker" : ticker})
        result[ticker] = {"Ticker": ticker, "Price": doc["Price"], "Industry": doc["Industry"], "Sector": doc["Sector"]}
    return result


  except:
    return "Unable to create summary report\n"

#Performance (Year)
@get('/stocks/api/v1.0/industryReport/<industry>')
def get_industry_top_five(industry):
  
  connection = MongoClient('localhost', 27017)
  db = connection['market']
  collection = db['stocks']

  topfive = []    # empty list

  try:
    results = collection.find({"Industry" : industry}).limit(5)
    for doc in results:
        topfive.append(doc["Ticker"])

    return json.loads(json.dumps(topfive, indent=4, default=json_util.default))


  except:
    return "Unable to generate top five list\n"




 
if __name__ == '__main__':
  #app.run(debug=True)
  run(host='localhost', port=8080)
  
