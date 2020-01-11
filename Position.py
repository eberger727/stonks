class Position:
    def __init__(self, ticker, call, strike_price, breakeven_price):
        self.ticker = ticker
        self.call = call
        self.strike_price = strike_price
        self.breakeven_price = breakeven_price

    def get_ticker(self):
        return self.ticker

    def get_call(self):
        return self.call

    def get_strike_price(self):
        return self.strike_price

    def get_breakeven_price(self):
        return self.breakeven_price
