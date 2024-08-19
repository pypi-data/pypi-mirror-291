import datetime
from typing import List
from .ccmobilebuildings import *
from ..Enums import UpgradeAvailability,AchivementsUnlock

class CCSaveMobileSettings:
    def __init__(self,data:dict) -> None:
        self._fancy = bool(data.get("fancy", 0))
        self._particles = bool(data.get("particles", 0))
        self._cookiepops = bool(data.get("cookiepops", 0))
        self._cookiewobble = bool(data.get("cookiewobble", 0))
        self._lowMotion = bool(data.get("lowMotion", 0))
        self._cursors = bool(data.get("cursors", 0))
        self._diagnostic = bool(data.get("diagnostic", 0))
        self._debug = bool(data.get("debug", 0))
        self._sound = bool(data.get("sound", 0))
        self._pan = bool(data.get("pan", 0))
        self._dislodge = bool(data.get("dislodge", 0))
        self._shadows = bool(data.get("shadows", 0))
        self._milk = bool(data.get("milk", 0))
        self._notScary = bool(data.get("notScary", 0))
    # Way too lazy to write allat 😭🙏
    @property
    def fancy(self):
        return self._fancy

    @property
    def particles(self):
        return self._particles

    @property
    def cookiepops(self):
        return self._cookiepops

    @property
    def cookiewobble(self):
        return self._cookiewobble

    @property
    def lowMotion(self):
        return self._lowMotion

    @property
    def cursors(self):
        return self._cursors

    @property
    def diagnostic(self):
        return self._diagnostic

    @property
    def debug(self):
        return self._debug

    @property
    def sound(self):
        return self._sound

    @property
    def pan(self):
        return self._pan

    @property
    def dislodge(self):
        return self._dislodge

    @property
    def shadows(self):
        return self._shadows

    @property
    def milk(self):
        return self._milk

    @property
    def notScary(self):
        return self._notScary

class CCSaveMobileBuildings:
    def __init__(self,data:dict) -> None:
        self.cursor = Cursor(data.get("Cursor"))
        self.grandma = Grandma(data.get("Grandma"))
        self.farm = Farm(data.get("Farm"))
        self.mine = Mine(data.get("Mine"))
        self.factory = Factory(data.get("Factory"))
        self.bank = Bank(data.get("Bank"))
        self.temple = Temple(data.get("Temple"))
        self.wizard_tower = WizardTower(data.get("Wizard tower"))
        self.shipment = Shipment(data.get("Shipment"))
        self.alchemy_lab = AlchemyLab(data.get("Alchemy lab"))
        self.portal = Portal(data.get("Portal"))
        self.time_machine = TimeMachine(data.get("Time machine"))
        self.antimatter_condenser = AntimatterCondenser(data.get("Antimatter condenser"))
        self.prism = Prism(data.get("Prism"))
        self.chancemaker = Chancemaker(data.get("Chancemaker"))
        self.fractal_engine = FractalEngine(data.get("Fractal engine"))
        self.javascript_console = JavascriptConsole(data.get("Javascript console"))
        self.idleverse = Idleverse(data.get("Idleverse"))
        self.cortex_baker = CortexBaker(data.get("Cortex baker"))
        self.you = You(data.get("You"))

class CCSaveMobileUpgrades:
    def __init__(self,upgrade,Availability:UpgradeAvailability) -> None:
        self.upgradeName = upgrade
        self.Availability = Availability

class CCSaveMobileAchivements:
    def __init__(self,achive,achivement:AchivementsUnlock) -> None:
        self.achive = achive
        self.Achivement= achivement
        
class CCSaveMobile:
    def __init__(self,data:dict) -> None:
        self.raw = data
        self.settings = data.get("settings")
        # Time and stuff
        self.time = data.get("time")
        self.runstarted = data.get("runStart")
        self.gamestarted = data.get("gameStart")
        self.seed = data.get("seed")
        # cookies
        self.currentcookies = data.get("cookies")
        self.earnedcookies = data.get("cookiesEarned")
        self.totalcookies = data.get("cookiesTotal")
        self.handmadecookies = data.get("cookiesHandmade")
        self.cookieclicks = data.get("cookieClicks")
        # builds
        self.buildings:dict = data.get("buildings")
        # idk
        self.gcClicks = data.get("gcClicks")
        self.gcClicksTotal = data.get("gcClicksTotal")
        self.gcMissed = data.get("gcMissed")
        self.reindeerClicks = data.get("reindeerClicks")
        self.reindeerClicksTotal = data.get("reindeerClicksTotal")
        self.reindeerMissed = data.get("reindeerMissed")
        self.elderWrath = data.get("elderWrath")
        self.pledges = data.get("pledges")
        self.pledgeT = data.get("pledgeT")
        self.wrinklersPopped = data.get("wrinklersPopped")
        self.cookiesSucked = data.get("cookiesSucked")
        self.cookiesReset = data.get("cookiesReset")
        self.heavenlyChips = data.get("heavenlyChips")
        self.heavenlyChipsSpent = data.get("heavenlyChipsSpent")
        self.resets = data.get("resets")
        self.seasonT = data.get("seasonT")
        self.seasonUses = data.get("seasonUses")
        self.season = data.get("season")
        self.santaLevel = data.get("santaLevel")
        self.dragonLevel = data.get("dragonLevel")
        self.dragonAura = data.get("dragonAura")
        self.dragonAura2 = data.get("dragonAura2")
        self.fortuneGC = data.get("fortuneGC")
        self.fortuneCPS = data.get("fortuneCPS")
        self.powerClicks = data.get("powerClicks")
        self.powerClicksTotal = data.get("powerClicksTotal")
        self.bgType = data.get("bgType")
        self.milkType = data.get("milkType")
        self.chimeType = data.get("chimeType")
        
        self.tippedN = data.get("tippedN")
        self.researchT = data.get("researchT")
        self.researchTM = data.get("researchTM")
        self.researchUpgrade = data.get("researchUpgrade")
        self.researchUpgradeLast = data.get("researchUpgradeLast")

        self.upgrades: dict = data.get("upgrades")
        self.achievs: dict = data.get("achievs")

    def _milliseconds_to_seconds(self, timestamp):
        if isinstance(timestamp, (int, float)) and timestamp > 1_000_000_000:
            return timestamp / 1000.0
        return timestamp
    


    @property
    def get_settings(self) -> CCSaveMobileSettings:
        """Gets settings"""
        return CCSaveMobileSettings(self.settings)
    
    # timestamps and all that stuff
    @property
    def get_time(self) -> datetime.datetime:
        """Gets the last time the player logged in"""
        time = self._milliseconds_to_seconds(self.time)
        return datetime.datetime.fromtimestamp(time)
    
    @property
    def get_run_started(self) -> datetime.datetime:
        """Gets the time when the run started"""
        runStartTime = self._milliseconds_to_seconds(self.runstarted)
        return datetime.datetime.fromtimestamp(runStartTime)

    @property
    def get_game_started(self) -> datetime.datetime:
        """Gets the time when the user started the game for the first time"""
        gameStartTime = self._milliseconds_to_seconds(self.gamestarted)
        return datetime.datetime.fromtimestamp(gameStartTime)
    # ze seed

    @property
    def get_seed(self) -> str:
        return self.seed
    
    # Cookies
    @property
    def get_Cookies(self) -> float:
        """Gets the current cookie amount that the player has"""
        return self.currentcookies
    
    @property
    def get_Total_Cookies(self) -> float:
        """Gets all total backed cookies"""
        return self.totalcookies
    
    @property
    def get_Earned_Cookies(self) -> float:
        """Tbh I have no idea what this is lol"""
        return self.earnedcookies
    
    @property
    def get_Clicked_Cookies(self) -> int:
        """Gets how much the player clicked the cookie"""
        return self.cookieclicks

    @property
    def get_Buildings(self) -> CCSaveMobileBuildings:
        return CCSaveMobileBuildings(data=self.buildings)

    @property
    def get_cookies(self) -> float:
        return self.currentcookies

    @property
    def get_gcClicks(self) -> int:
        return self.gcClicks

    @property
    def get_gcClicksTotal(self) -> int:
        return self.gcClicksTotal

    @property
    def get_gcMissed(self) -> int:
        return self.gcMissed

    @property
    def get_reindeerClicks(self) -> int:
        return self.reindeerClicks

    @property
    def get_reindeerClicksTotal(self) -> int:
        return self.reindeerClicksTotal

    @property
    def get_reindeerMissed(self) -> int:
        return self.reindeerMissed

    @property
    def get_elderWrath(self) -> int:
        return self.elderWrath

    @property
    def get_pledges(self) -> int:
        return self.pledges

    @property
    def get_pledgeT(self) -> int:
        return self.pledgeT

    @property
    def get_wrinklersPopped(self) -> int:
        return self.wrinklersPopped

    @property
    def get_cookiesSucked(self) -> float:
        return self.cookiesSucked

    @property
    def get_cookiesReset(self) -> float:
        return self.cookiesReset

    @property
    def get_heavenlyChips(self) -> int:
        return self.heavenlyChips

    @property
    def get_heavenlyChipsSpent(self) -> int:
        return self.heavenlyChipsSpent

    @property
    def get_resets(self) -> int:
        return self.resets

    @property
    def get_seasonT(self) -> int:
        return self.seasonT

    @property
    def get_seasonUses(self) -> int:
        return self.seasonUses

    @property
    def get_season(self) -> str:
        return self.season

    @property
    def get_santaLevel(self) -> int:
        return self.santaLevel

    @property
    def get_dragonLevel(self) -> int:
        return self.dragonLevel

    @property
    def get_dragonAura(self) -> int:
        return self.dragonAura

    @property
    def get_dragonAura2(self) -> int:
        return self.dragonAura2

    @property
    def get_fortuneGC(self) -> int:
        return self.fortuneGC

    @property
    def get_fortuneCPS(self) -> int:
        return self.fortuneCPS

    @property
    def get_powerClicks(self) -> int:
        return self.powerClicks

    @property
    def get_powerClicksTotal(self) -> int:
        return self.powerClicksTotal

    @property
    def get_bgType(self) -> int:
        return self.bgType

    @property
    def get_milkType(self) -> int:
        return self.milkType

    @property
    def get_chimeType(self) -> int:
        return self.chimeType

    @property
    def get_currentcookies(self) -> float:
        return self.currentcookies
    
    @property
    def get_earnedcookies(self) -> float:
        return self.earnedcookies

    @property
    def get_totalcookies(self) -> float:
        return self.totalcookies

    @property
    def get_handmadecookies(self) -> float:
        return self.handmadecookies

    @property
    def get_tippedN(self) -> float:
        return self.tippedN

    @property
    def get_researchT(self) -> float:
        return self.researchT

    @property
    def get_researchTM(self) -> float:
        return self.researchTM

    @property
    def get_researchUpgrade(self) -> float:
        return self.researchUpgrade

    @property
    def get_researchUpgradeLast(self) -> float:
        return self.researchUpgradeLast
    
    @property
    def get_upgrades(self) -> List[CCSaveMobileUpgrades]:
        upgrades: List[CCSaveMobileUpgrades] = []
        for upgrade_key, availabile in self.upgrades.items():
            try:
                upgrade = int(upgrade_key)
                availability_enum = UpgradeAvailability(availabile)
            except:
                availability_enum = UpgradeAvailability.NOTAVAILABLE
            upgrades.append(CCSaveMobileUpgrades(upgrade=upgrade, Availability=availability_enum))
        return upgrades
    
    @property
    def get_achievements(self) -> List[CCSaveMobileAchivements]:
        achivements: List[CCSaveMobileAchivements] = []
        for achievs_key, achivement in self.achievs.items():
            try:
                achive = int(achievs_key)
                achivement_enum = AchivementsUnlock(achivement)
            except:
                achivement_enum = AchivementsUnlock.LOCKED
            achivements.append(CCSaveMobileAchivements(achive=achive, achivement=achivement_enum))
        return achivements
    
    # Time stuff
    def set_time(self,value:datetime.datetime) -> None:
        # Why does Cookie Clicker use Milisec 😭🙏
        milisec_unix = value.timestamp() * 1000
        self.time = milisec_unix

    def set_game_started(self,value:datetime.datetime) -> None:
        milisec_unix = value.timestamp() * 1000
        self.gamestarted = milisec_unix

    def set_run_started(self,value:datetime.datetime) -> None:
        milisec_unix = value.timestamp() * 1000
        self.runstarted = milisec_unix

    # Cookies
    def set_cookies(self, value: float) -> None:
        self.currentcookies = value

    def set_earnedcookies(self, value: float) -> None:
        self.earnedcookies = value

    def set_totalcookies(self, value: float) -> None:
        self.totalcookies = value

    def set_handmadecookies(self, value: float) -> None:
        self.handmadecookies = value

    def set_cookiesSucked(self, value: float) -> None:
        self.cookiesSucked = value

    def set_cookiesReset(self, value: float) -> None:
        self.cookiesReset = value

    def set_heavenlyChips(self, value: int) -> None:
        self.heavenlyChips = value


    def set_heavenlyChipsSpent(self, value: int) -> None:
        self.heavenlyChipsSpent = value

    # I really dont know what GC Clicks mean
    def set_gcClicks(self, value: int) -> None:
        self.gcClicks = value

    def set_gcClicksTotal(self, value: int) -> None:
        self.gcClicksTotal = value


    def set_gcMissed(self, value: int) -> None:
        self.gcMissed = value

    # Christmas Stuff
    def set_reindeerClicks(self, value: int) -> None:
        self.reindeerClicks = value


    def set_reindeerClicksTotal(self, value: int) -> None:
        self.reindeerClicksTotal = value


    def set_reindeerMissed(self, value: int) -> None:
        self.reindeerMissed = value

    # Uhhh
    def set_elderWrath(self, value: int) -> None:
        self.elderWrath = value


    def set_pledges(self, value: int) -> None:
        self.pledges = value


    def set_pledgeT(self, value: int) -> None:
        self.pledgeT = value

    # What the hell is this suppose to mean 
    def set_wrinklersPopped(self, value: int) -> None:
        self.wrinklersPopped = value

    def set_resets(self, value: int) -> None:
        self.resets = value


    def set_seasonT(self, value: int) -> None:
        self.seasonT = value


    def set_seasonUses(self, value: int) -> None:
        self.seasonUses = value


    def set_season(self, value: str) -> None:
        self.season = value


    def set_santaLevel(self, value: int) -> None:
        self.santaLevel = value


    def set_dragonLevel(self, value: int) -> None:
        self.dragonLevel = value


    def set_dragonAura(self, value: int) -> None:
        self.dragonAura = value



    def set_dragonAura2(self, value: int) -> None:
        self.dragonAura2 = value


    def set_fortuneGC(self, value: int) -> None:
        self.fortuneGC = value


    def set_fortuneCPS(self, value: int) -> None:
        self.fortuneCPS = value


    def set_powerClicks(self, value: int) -> None:
        self.powerClicks = value


    def set_powerClicksTotal(self, value: int) -> None:
        self.powerClicksTotal = value


    def set_bgType(self, value: int) -> None:
        self.bgType = value


    def set_milkType(self, value: int) -> None:
        self.milkType = value


    def set_chimeType(self, value: int) -> None:
        self.chimeType = value

    def set_currentcookies(self, value: float) -> None:
        self.currentcookies = value

    def set_earnedcookies(self, value: float) -> None:
        self.earnedcookies = value

    def set_totalcookies(self, value: float) -> None:
        self.totalcookies = value

    def set_handmadecookies(self, value: float) -> None:
        self.handmadecookies = value

    def set_tippedN(self, value: float) -> None:
        self.tippedN = value

    def set_researchT(self, value: float) -> None:
        self.researchT = value

    def set_researchTM(self, value: float) -> None:
        self.researchTM = value

    def set_researchUpgrade(self, value: float) -> None:
        self.researchUpgrade = value

    def set_researchUpgradeLast(self, value: float) -> None:
        self.researchUpgradeLast = value