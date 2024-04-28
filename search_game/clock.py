from search_game import gameglobals


class Ticker:
    seconds: float
    thresh: float

    def __init__(self, thresh: float):
        self.seconds = 0
        self.thresh = thresh

    def tick(self) -> bool:
        self.seconds += gameglobals.dt
        if self.seconds > self.thresh:
            self.seconds = 0
            return True
        return False
