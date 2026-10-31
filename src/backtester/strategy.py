class BuyAndHold:
    """Buys once on the first day, then holds."""

    def __init__(self) -> None:
        self.bought = False

    def on_bar(self, history) -> str:
        if not self.bought:
            self.bought = True
            return "buy"
        return "hold"

class MovingAverageCrossover:
    """Buy when the short average is above the long average, else sell."""

    def __init__(self, short_window: int, long_window: int) -> None:
        self.short_window = short_window
        self.long_window = long_window

    def on_bar(self, history) -> str:
        if len(history) < self.long_window:
            return "hold"
        close = history["Close"]
        short_avg = close.rolling(self.short_window).mean().iloc[-1]
        long_avg = close.rolling(self.long_window).mean().iloc[-1]
        if short_avg > long_avg:
            return "buy"
        return "sell"