

class CCSavePC:
    def __init__(self,data:list) -> None:
        self.gameVersion = data[0]
        self.bakeryInfo = data[2]
        self.startDate = self.bakeryInfo[0] # Time and date of the current ascension's start.
        self.fullDate = self.bakeryInfo[1] # Time and date of the whole game's start.
        self.lastDate = self.bakeryInfo[2] # Time and date of the time we last opened the game.
        self.bakeryName = self.bakeryInfo[3] # String with the bakery's name.
        self.gameData = data[4] # Game data such as cookies and all that stuff
        self.cookies = self.gameData[0]  # Total cookies
        self.cookiesEarned = self.gameData[1]  # Total cookies earned
        self.cookieClicks = self.gameData[2]  # Cookie clicks
        self.goldenCookieClicks = self.gameData[3]  # Golden cookie clicks
        self.cookiesMadeByClicking = self.gameData[4]  # Cookies made by clicking
        self.goldenCookiesMissed = self.gameData[5]  # Golden cookies missed
        self.backgroundType = self.gameData[6]  # Background type
        self.milkType = self.gameData[7]  # Milk type
        self.cookiesFromPastRuns = self.gameData[8]  # Cookies from past runs
        self.elderWrath = self.gameData[9]  # Elder wrath
        self.pledges = self.gameData[10]  # Pledges
        self.pledgeTimeLeft = self.gameData[11]  # Pledge time left
        self.currentlyResearching = self.gameData[12]  # Currently researching
        self.researchTimeLeft = self.gameData[13]  # Research time left
        self.ascensions = self.gameData[14]  # Ascensions
        self.goldenCookieClicksThisRun = self.gameData[15]  # Golden cookie clicks (this run)
        self.cookiesSuckedByWrinklers = self.gameData[16]  # Cookies sucked by wrinklers
        self.wrinklesPopped = self.gameData[17]  # Wrinkles popped
        self.santaLevel = self.gameData[18]  # Santa level
        self.reindeerClicked = self.gameData[19]  # Reindeer clicked
        self.seasonTimeLeft = self.gameData[20]  # Season time left
        self.seasonSwitcherUses = self.gameData[21]  # Season switcher uses
        self.currentSeason = self.gameData[22]  # Current season
        self.cookiesContainedInWrinklers = self.gameData[23]  # Amount of cookies contained in wrinklers
        self.numberOfWrinklers = self.gameData[24]  # Number of wrinklers
        self.prestigeLevel = self.gameData[25]  # Prestige level
        self.heavenlyChips = self.gameData[26]  # Heavenly chips
        self.heavenlyChipsSpent = self.gameData[27]  # Heavenly chips spent
        self.heavenlyCookies = self.gameData[28]  # Heavenly cookies
        self.ascensionMode = self.gameData[29]  # Ascension mode