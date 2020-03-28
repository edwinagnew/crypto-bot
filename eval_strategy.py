import numpy as np
import pandas as pd 
from datetime import datetime

import Stategies


class Eval:

	def __init__(self, nstrat, data_path = "data/kraken_cleaned.csv", verbose=False):
		self.stat = Stategies.Strategy(nstrat, rand_prop=False)
		#self.strategy_number = nstrat

		self.df = pd.read_csv(data_path)[2100:]

		self.cash = 1000
		self.start_cash = self.cash
		self.btc = 0


		self.actions = {"purchases": [], "sales": []}


		self.verbose = verbose


		self.evaluate_strategy()


	def evaluate_strategy(self):
		"""Goes through every single price in the dataset and simulates whether the strategy would buy or sell at that price and calculates profit
		"""
		last_price = 0
		for index, row in self.df.iterrows():
			valid = False
			if self.verbose: print(row['Weighted_Price'], "prev:", last_price, "change: ", row['Weighted_Price'] - last_price)
			response = self.stat.eval(row['Weighted_Price']) #response will be in format {'BUY': amount} , {'SELL': amount} or {'NOTHING': None} where amount is proportion of current assets
			if "SELL" in response:
				valid = self.sell(response["SELL"] * self.btc, row['Weighted_Price'])
			elif "BUY" in response:
				valid = self.buy(response["BUY"] * self.cash, row['Weighted_Price'])
			if valid and "reason" in response: print("because" , response["reason"])
			last_price = row['Weighted_Price']

		self.sell_all(row["Weighted_Price"])

		print("Finished: made ", len(self.actions["purchases"]), " purchases and ", len(self.actions["sales"]), " sales")

		print("Finished evaluating: CASH: ", self.start_cash, " -> ", self.cash)


	def buy(self, amount, price):
		#API CALL
		if self.cash == 0:
			if self.verbose: print("tried to buy but youre broke son")
			return False

		else:
			self.cash -= amount
			self.btc += amount/price

			time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

			purchase = time + " Buying " + str(amount/price) + "BTC at price, " + str(price) + "USD"
			print(purchase)
			if self.verbose: 
				print("CASH:", self.cash, "USD, BTC:", self.btc)
			self.actions['purchases'].append(purchase)
			return True




	def sell(self, amount, price):
		#API CALL
		if self.btc == 0:
			if self.verbose: print("tried to sell but havent got any mate")
			return False

		else:
			self.cash += amount * price
			self.btc -= amount

			time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

			sale = time + " Selling " + str(amount) + "BTC at price, " + str(price) + "USD"
			print(sale)
			if self.verbose: 
				print("CASH:",self.cash, "USD, BTC:", self.btc)
			self.actions['sales'].append(sale)
			return True


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













