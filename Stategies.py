import random
class Strategy:


    def __init__(self, nstrat, t_i=60, rand_prop = False):
        self.last_price = 0
        self.TIME_INTERVAL = t_i

        eval_dict = {1 : self.basic_strat, 2: self.basic_strat_rand, 3: self.strat_1}
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
            return {"BUY": 100}
