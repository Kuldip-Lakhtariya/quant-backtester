class BuyAndHold:
    """Buys once on the first day, then holds."""

    def __init__(self) -> None:
        self.bought = False

    def on_bar(self, history) -> str:
        if not self.bought:
            self.bought = True
            return "buy"
        return "hold"