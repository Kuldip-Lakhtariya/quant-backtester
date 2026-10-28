class Portfolio:
    def __init__(self, cash: float) -> None:
        self.cash = cash
        self.shares = 0

    def buy_all(self, price: float) -> None:
        qty = int(self.cash // price)
        self.shares += qty
        self.cash -= qty * price

    def sell_all(self, price: float) -> None:
        self.cash += self.shares * price
        self.shares = 0

    def value(self, price: float) -> float:
        return self.cash + self.shares * price