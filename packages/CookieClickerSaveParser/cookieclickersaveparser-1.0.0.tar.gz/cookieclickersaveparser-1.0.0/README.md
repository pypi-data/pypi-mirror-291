Simple Cookie Clicker Save Parser for pc and mobile save files

### Currently mobile saves are the most supported save right now, since parsing pc saves is pretty much tricky since they dont use jsons

how to install
```
pip install git+https://github.com/username/repository.git
```

Usage:
```py
from CCParse import CCDecode, SaveType, ccpc,ccmobile
from CCParse.models.ccmobile import CCSaveMobile
from CCParse.models.ccpc import CCSavePC
import os
import datetime
decoder = CCDecode()


def Parse_Mobile_Save():
    with open("CookieClickerSaveMobileExample.txt",mode="r") as file:
        decoded_save:CCSaveMobile = decoder.decode(file.read(),type=SaveType.MOBILE)

        print(f"""
        Game First Time Started: {decoded_save.get_game_started}
        Last Login: {decoded_save.get_time}
        Run Started: {decoded_save.get_run_started}
        Seed: {decoded_save.get_seed}

        """)

        print(f"""
        Current Cookies: {decoded_save.get_cookies}
        Clicked Cookies: {decoded_save.get_Clicked_Cookies}
        Earned Cookies: {decoded_save.get_Earned_Cookies}
        Total Cookies: {decoded_save.get_Total_Cookies}

        """)

        for upgrade in decoded_save.get_upgrades:
            print(f"{upgrade.upgradeName}: {upgrade.Availability}")

        print("")

        for achivement in decoded_save.get_achievements:
            print(f"""{achivement.achive}: {achivement.Achivement}""")

        print("")

            
        print(f"""
        Cursor:
            Bought: {decoded_save.get_Buildings.cursor.bought}
            Amount: {decoded_save.get_Buildings.cursor.amount}
            Amount Max: {decoded_save.get_Buildings.cursor.amountMax}
            Cookies Made: {decoded_save.get_Buildings.cursor.cookiesmade}

        Grandma:
            Bought: {decoded_save.get_Buildings.grandma.bought}
            Amount: {decoded_save.get_Buildings.grandma.amount}
            Amount Max: {decoded_save.get_Buildings.grandma.amountMax}
            Cookies Made: {decoded_save.get_Buildings.grandma.cookiesmade}
        """)


def Parse_PC_Save():
    with open("GexBakery.txt",mode="r") as file:
        decoded_save:CCSavePC = decoder.decode(file.read(),type=SaveType.PC)
        print(decoded_save.cookies)
        print(decoded_save.cookiesEarned)
        print(decoded_save.cookiesSuckedByWrinklers)
        
Parse_Mobile_Save()
Parse_PC_Save()
```