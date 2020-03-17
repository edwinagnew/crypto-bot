class Strategy:

    TIME_INTERVAL = 60

    def __init__(self):

    def basic_strat(self, new_price):
    """
    Basic Strategy will:
        SELL when the price is larger than the previous price
        BUY when the price is less than the previous price
    """
        last_price = 0

        if(new_price > last_price):
            last_price = new_price
            return {"SELL": 1}

        elif(new_price < last_price):
            last_price = new_price
            return {"BUY": 1}

        else(new_price == last_price):
            return {"NOTHING": 0}

    def strat_1(self, new_price):
        """
        Strategy 1 will:
            BUY: When the graph has been falling for a bit and then platops off
            SELL: When the graph has been increasing for a bit and then platos off
        """
        last_price = 0
        last_gradient = 1
        current_gradient = (new_price - last_price)/TIME_INTERVAL

        if(current_gradient < 0.5 and current_gradient > -0.5):
            return {"BUY": 100}
