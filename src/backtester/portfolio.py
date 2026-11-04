class Portfolio:
    def __init__(self, cash: float, fee_rate: float = 0.0, slippage_rate: float = 0.0) -> None:
        self.cash = cash
        self.shares = 0
        self.fee_rate = fee_rate            
        self.slippage_rate = slippage_rate  

    def buy_all(self, price: float) -> None:
        fill_price = price * (1 + self.slippage_rate)   
        cost_per_share = fill_price * (1 + self.fee_rate)  
        qty = int(self.cash // cost_per_share)
        trade_value = qty * fill_price
        fee = trade_value * self.fee_rate
        self.shares += qty
        self.cash -= trade_value + fee

    def sell_all(self, price: float) -> None:
        fill_price = price * (1 - self.slippage_rate)  # we get a worse (lower) price
        proceeds = self.shares * fill_price
        fee = proceeds * self.fee_rate
        self.cash += proceeds - fee
        self.shares = 0

    def value(self, price: float) -> float:
        return self.cash + self.shares * price