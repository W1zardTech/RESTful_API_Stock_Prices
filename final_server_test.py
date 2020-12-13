#!/usr/bin/python
import json
from bson import json_util
from pymongo.collection import ReturnDocument
import bottle
from bottle import route, run, get, request, abort, post, put, delete
import datetime
from pymongo import MongoClient
import pymongo.errors
import os

def test_REST_API():
  # test create a ticker symbol
  os.system("curl -H 'Content-Type: application/json' -X POST -d '{\"Sector\" : \"Healthcare\", \"Price\" : 100}' http://localhost:8080/stocks/api/v1.0/createStock/TEST_TICKER")

  # retrieve the ticker symbol to make sure it was stored in database
  os.system("curl http://localhost:8080/stocks/api/v1.0/getStock/TEST_TICKER")

  # update the ticker symbol that was previously created
  os.system("curl -H \"Content-Type: application/json\" -X PUT -d '{\"Sector\" : \"Oil and Gas\", \"Price\" : 75}' http://localhost:8080/stocks/api/v1.0/updateStock/TEST_TICKER")

  # delete the ticker symbol
  os.system("curl -X DELETE http://localhost:8080/stocks/api/v1.0/deleteStock/TEST_TICKER")


 
if __name__ == '__main__':
  test_REST_API()  # run the API tests
  
