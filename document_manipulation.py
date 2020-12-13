import json
from bson import json_util
from pymongo import MongoClient
import pymongo.errors
from pymongo.collection import ReturnDocument
import os
import pprint


connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

def insert_document(document):
	try:
		result = collection.save(document)
		return True

	except:
		return False

def update_document(ticker, volume):
	try:
		result = collection.find_one_and_update({"Ticker": ticker}, {"$set": {"Volume": volume}}, return_document=ReturnDocument.AFTER)
		return result

	except pymongo.errors.OperationFailure as oe:
		return oe

def delete_document(ticker):
	try:
		result = collection.delete_one({"Ticker": ticker})
		return result

	except pymongo.errors.OperationFailure as oe:
		return oe

def main():
	myDocument = {"Ticker": "MERLIN",  "Price": 100.00, "Profit Margin" : 0.25, "Institutional Ownership": 0.65}
	myFakeDoc = "This is not a real document"
	result = insert_document(myDocument)
	print(result) #prints True
 	result = insert_document(myFakeDoc)
 	print(result) #prints False

	# print the newly created document for verification
	print("The newly inserted document:\n")
	pprint.pprint(collection.find_one({"Ticker": "MERLIN"}))

	print("\nThe updated document:\n")
	result = update_document("MERLIN", 100000) #set the volume to 100,000
	pprint.pprint(result)  #prints updated document

	# Delete the document with ticker symbol BRLI
	result = delete_document("BRLI")
	print(result)    # print the result

if __name__ == "__main__":
	main()
