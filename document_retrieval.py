import json
from bson import json_util
from pymongo import MongoClient
import pymongo.errors
from pymongo.collection import ReturnDocument
import os


connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

def total_shares_outstanding(sector):

		result_dict = {}
		result = db.stocks.aggregate([
			{"$match": {"Sector" : "Healthcare"}},
			{"$group": {"_id": {"Industry" : "$Industry"}, 
			           "total shares" : {"$sum" : "$Shares Outstanding"}}} 
                   	]) 
		
		for doc in result:
			print(doc)


def count_stocks_between_moving_avg(low, high):
	try:
		result = collection.find({"50-Day Simple Moving Average": {"$gte":low, "$lte":high}}).count()
		return result

	except:
		return 0


def return_tickers_for_industry(industry):
	tickers = []  # empty list
	try:
		result = collection.find({"Industry": industry})
		for doc in result:
			tickers.append(doc["Ticker"])		
		return tickers

	except:
		return tickers    # empty list


def main():

	# count stocks with moving averages between the provided values 
	result1 = count_stocks_between_moving_avg(0.1, 0.2)
	result2 = count_stocks_between_moving_avg(0.2, 0.3)
	result3 = count_stocks_between_moving_avg(0.3, 0.4)

	print("Number of stocks with moving avg between 0.1 and 0.2: " + str(result1))    # print the result
	print("Number of stocks with moving avg between 0.2 and 0.3: " + str(result2))    # print the result
	print("Number of stocks with moving avg between 0.3 and 0.4: " + str(result3))    # print the result

	# get a list of ticker symbols for the given industry
	tickers = return_tickers_for_industry("Medical Laboratories & Research")
	print(tickers)

	# get total shares outstanding for Healthcare
	total_shares_outstanding("Healthcare")

	# get total shares outstanding for Basic Materials
	total_shares_outstanding("Basic Materials")
	


if __name__ == "__main__":
	main()
