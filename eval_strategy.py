import numpy as np
import pandas as pd 
from datetime import datetime

import Stategies


class Eval:

	def __init__(self, nstrat, data_path = "data/kraken_cleaned.csv", verbose=False):
		self.stat = Stategies.Strategy(nstrat, rand_prop=False)
		#self.strategy_number = nstrat

		self.df = pd.read_csv(data_path)

		self.cash = 500
		self.btc = 0


		self.actions = {"purchases": [], "sales": []}


		self.verbose = verbose


		self.evaluate_strategy()


	def evaluate_strategy(self):
		"""Goes through every single price in the dataset and 
		"""
		last_price = 0
		for index, row in self.df.iterrows():
			if self.verbose: print(row['Weighted_Price'], "prev:", last_price, "change: ", row['Weighted_Price'] - last_price)
			response = self.stat.eval(row['Weighted_Price']) #response will be in format {'BUY': amount} , {'SELL': amount} or {'NOTHING': None} where amount is proportion of current assets
			if "SELL" in response:
				self.sell(response["SELL"] * self.btc, row['Weighted_Price'])
			elif "BUY" in response:
				self.buy(response["BUY"] * self.cash, row['Weighted_Price'])
			last_price = row['Weighted_Price']

		self.sell_all(row["Weighted_Price"])

		print("Finished evaluating: CASH: 500 ->", self.cash)


	def buy(self, amount, price):
		#API CALL
		if self.cash == 0:
			print("tried to buy but youre broke son")

		else:
			self.cash -= amount
			self.btc += amount/price

			time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

			purchase = time + " Buying " + str(amount/price) + "BTC at price, " + str(price) + "USD"
			if self.verbose: 
				print(purchase)
				print("CASH:", self.cash, "USD, BTC:", self.btc)
			self.actions['purchases'].append(purchase)




	def sell(self, amount, price):
		#API CALL
		if self.btc == 0:
			print("tried to sell but havent got any mate")

		else:
			self.cash += amount * price
			self.btc -= amount

			time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

			sale = time + " Selling " + str(amount) + "BTC at price, " + str(price) + "USD"
			if self.verbose: 
				print(sale)
				print("CASH:",self.cash, "USD, BTC:", self.btc)
			self.actions['sales'].append(sale)


	def sell_all(self,price):
		#API call
		self.cash += self.btc * price
		self.btc = 0

		time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

		sale = time + " Selling all " + str(self.btc) + "BTC at price, " + str(price) + "USD"
		if self.verbose: 
			print(sale)
			print("CASH:" , self.cash, "USD, BTC:", self.btc)
		self.actions['sales'].append(sale)













