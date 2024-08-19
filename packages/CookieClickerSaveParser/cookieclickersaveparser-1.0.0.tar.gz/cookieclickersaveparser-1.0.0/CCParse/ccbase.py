
class CCBaseBuildingMobile:
    def __init__(self,data:dict) -> None:
        self.amount = data.get("amount")
        self.amountMax = data.get("amountMax")
        self.bought = data.get("bought")
        self.cookiesmade = data.get("cookiesMade")
    
    @property
    def get_amount(self):
        return self.amount

    @property
    def get_max_amount(self):
        return self.amountMax
    

    @property
    def get_bought_buildings(self):
        return self.bought
    
    @property
    def get_cookies(self):
        return self.cookiesmade