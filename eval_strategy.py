import numpy as np
import pandas as pd 
from datetime import datetime


Class Eval:

	def __init__(strategy, data_path = "data/kraken_cleaned.csv", verbose=False):
		self.strategy = strategy
		self.df = pd.read_csv(data_path)

		self.cash = 500
		self.btc = 0

		self.purchases = []
		self.sales = []

		self.verbose = verbose


		self.evlauate_strategy()



	def update(self, new_price):
		print("soon")

	def evaluate_strategy(self):
		for index, row in self.df.iterrows():
			response = self.strategy(row['Weighted_Price']) #response will be in format {'BUY': amount} , {'SELL': amount} or {'NOTHING': None} where amount is proportion of current assets
			if "SELL" in response:
				self.sell(response["SELL"] * self.btc, row['Weighted_Price'])
			elif "BUY" in response:
				self.buy(response["BUY"] * self.cash, row['Weighted_Price'])

		self.sell_all(row["Weighted_Price"])

		print("Finished evaluating: CASH: 500 ->", self.cash)


	def buy(self, amount, price):
		#API CALL

		self.cash -= amount * price
		self.btc += price/amount

		time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

		purchase = time + "Buying " + str(price/amount) + "BTC at price, " + str(price) + "USD"
		if self.verbose: 
			print(purchase)
			print("CASH:" self.cash, "USD, BTC:", self.btc)
		self.purchases.append(purchase)




	def sell(self, amount, price):
		#API CALL

		self.cash += amount * price
		self.btc -= price/amount

		time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

		sale = time + "Selling " + str(price/amount) + "BTC at price, " + str(price) + "USD"
		if self.verbose: 
			print(sale)
			print("CASH:" self.cash, "USD, BTC:", self.btc)
		self.sales.append(sale)


	def sell_all(self,price):
		#API call
		self.cash += self.btc * price
		self.btc = 0

		sale = time + "Selling all " + str(self.btc) + "BTC at price, " + str(price) + "USD"
		if self.verbose: 
			print(sale)
			print("CASH:" self.cash, "USD, BTC:", self.btc)
		self.sales.append(sale)













