import random
import numpy as np
class Strategy:


    def __init__(self, nstrat, t_i=60, rand_prop = False):

        self.last_prices = []
        self.last_grad = (0, 0)

        self.last_price = 0
        self.TIME_INTERVAL = t_i

        self.buy_price = None

        eval_dict = {1 : self.basic_strat, 2: self.basic_strat_rand, 3: self.strat_1, 4: self.buy_hard_sell_simple}
        self.eval = eval_dict[nstrat]
        s_p=0.3
        b_p=0.3

        if rand_prop:
            s_p = random.uniform(0,1)
            b_p = random.uniform(0,1) 
            print("With buy and sell", s_p, b_p)

        self.sell_prop = s_p 
        self.buy_prop = b_p

    def basic_strat(self, new_price):
        """
        Basic Strategy will:
        SELL when the price is larger than the previous price
        BUY when the price is less than the previous price
        """

        if new_price > self.last_price:
            self.last_price = new_price
            return {"SELL": self.sell_prop}

        elif new_price < self.last_price:
            self.last_price = new_price
            return {"BUY": self.buy_prop}

        else:
            self.last_price = new_price
            return {"NOTHING": 0}

    def basic_strat_rand(self, new_price):
        sell_p = random.uniform(0, 1)
        buy_p = random.uniform(0, 1)
        return self.basic_strat(new_price,sell_prop=sell_p, buy_prop=buy_p)




    def strat_1(self, new_price):
        """
        Strategy 1 will:
        BUY: When the graph has been falling for a bit and then platops off
        SELL: When the graph has been increasing for a bit and then platos off
        """
        last_price = 0
        last_gradient = 1
        current_gradient = (new_price - last_price)/self.TIME_INTERVAL

        if current_gradient < 0.5 and current_gradient > -0.5:
            return {"BUY": 0.1}


    def grad_strat(self, new_price):

        self.last_prices.append(new_price)

        grad = (self.last_prices[-1] - self.last_prices[-2])/self.TIME_INTERVAL

        last_g = self.last_grad[0]

        if np.sign(grad) == np.sign(self.last_grad[0]):
            self.last_grad = (grad, self.last_grad + 1)
        else:
            self.last_grad = (grad, 1)

        second_grad = (grad - last_g)/self.TIME_INTERVAL

        if second_grad < 0:
            return {"BUY": 0.2}
        elif second_grad > 0:
            return {"SELL": 0.2}

    def buy_hard_sell_simple(self, new_price):
        """Sells when price is 100 higher than buy price, buys when a drop plateau is (probably) approaching
        """ 
        """
                             try self.last_prices:
                                 pass
                             except NameError:
                                 self.last_prices = []"""

        if self.buy_price and new_price - self.buy_price > 100:
            return {"SELL": 1, "reason": "because bought at " + str(self.buy_price) + "and now " + str(new_price)}

        self.last_prices.append(new_price)
        grads = self.get_grads(self.last_prices[-15:])
        if np.mean(grads) < 0 and grads[-1] < 0 and grads[-1] > -0.5:
            self.buy_price = new_price
            return {"BUY": 1}


        return {"NOTHING": 0}


    def get_grads(self, prices):
        grads = []
        for i in range(1,len(prices)):
            grads.append(prices[i] - prices[i-1])
        return grads
        
       


            



