#!/usr/bin/env python3
import random;import subprocess;Playing = True;LimitX = 10;LimitY = 10;Mines = 10;SafeStart = True
def Play():
    global LimitX,LimitY,Mines,SafeStart
    Minesweeper = {};Shown = {};Flagged = {};GameActive = True;Win = False;FlagMode = False;PlayerQuits = False;EndMessage = "";Colors = {"0": '3', "1": '94', "2": '32', "3": '91', "4": '34', "5": '31', "6": '36', "7": '30', "8": '37', "M": '41', "X": '0', "F": '7'}
    def RevealTile(STile):
        if Shown[STile] == False:
            posi = STile.find(", ");Shown[STile] = True
            if Minesweeper[STile] == 0:
                for xo in range(int(STile[0:posi])-1,int(STile[0:posi])+2):
                    for yo in range(int(STile[posi+2:])-1,int(STile[posi+2:])+2):
                        ChainedTile = str(xo) + ", " + str(yo)
                        if ChainedTile in Minesweeper: RevealTile(ChainedTile)
    def RevealBoard():
        subprocess.run('clear')
        for yp in range(1,LimitY + 1):
            Row = ""
            for xp in range(1,LimitX + 1):
                Tiler = str(xp) + ", " + str(yp);Emit = str(Minesweeper[Tiler])
                if Shown[Tiler] == False:Emit = "X"
                if Flagged[Tiler] == True:Emit = "F"
                if GameActive == False and Minesweeper[Tiler] == "M":Emit = "F" if Win == True else "M"
                Row += '\033[' + Colors[Emit] +'m'+ Emit + '\033[0m' + " "
            print(Row)
        print("")   
    for x in range(1,LimitX + 1):
        for y in range(1,LimitY + 1): Tile = str(x) + ", " + str(y);Minesweeper[Tile] = 0;Shown[Tile] = False;Flagged[Tile] = False
    RevealBoard()
    TileNoExists = True;ChosenTile = ""
    while TileNoExists:
        TheTile = input("Enter A Tile (X, Y):" )
        if TheTile in Minesweeper:ChosenTile = TheTile;TileNoExists = False
        else:print("Tile doesnt exist! try again.")
    NoNoSquares = {}
    pos = ChosenTile.find(", ")
    for xo in range(int(ChosenTile[0:pos])-1,int(ChosenTile[0:pos])+2):
        for yo in range(int(ChosenTile[pos+2:])-1,int(ChosenTile[pos+2:])+2):
            Tiled = str(xo) + ", " + str(yo)
            if Tiled in Minesweeper: NoNoSquares[Tiled] = True
    if SafeStart == False:NoNoSquares = {}
    if Mines >= LimitX * LimitY - len(NoNoSquares):NoNoSquares = {}
    if Mines >= LimitX * LimitY: Mines = LimitX * LimitY
    for r in range(1,Mines + 1):
        xa = 0;ya = 0;AlreadyMine = True
        while AlreadyMine:
            xa = random.randint(1,LimitX);ya = random.randint(1,LimitY)
            if Minesweeper[str(xa) + ", " + str(ya)] != "M" and not str(xa) + ", " + str(ya) in NoNoSquares: AlreadyMine = False
        Mine = str(xa) + ", " + str(ya);Minesweeper[Mine] = "M"
        for xi in range(xa-1,xa+2):
            for yi in range(ya-1,ya+2):
                Tiled = str(xi) + ", " + str(yi)
                if Tiled in Minesweeper and Minesweeper[Tiled] != "M": Minesweeper[Tiled] += 1
    RevealTile(ChosenTile)
    AllShown = True
    for xe in range(1,LimitX + 1):
        for ye in range(1,LimitY + 1):
            Tile = str(xe) + ", " + str(ye)
            if Shown[Tile] != True and Minesweeper[Tile] != "M": AllShown = False
            if Shown[Tile] == True and Minesweeper[Tile] == "M": AllShown = False;GameActive = False
    if AllShown == True: Win = True;GameActive = False
    RevealBoard()
    while GameActive == True:
        TileNoExists = True;ChosenTile = ""
        while TileNoExists:
            TheTile = input(" A Tile to Open (X, Y) [Write -f to Toggle on flag mode or -q to Quit]:" if FlagMode == False else "Enter A Tile to Flag (X, Y) [Write -f to Toggle off flag mode or -q to Quit]:")
            if TheTile == "-q":
                GameActive = False;TileNoExists = False;PlayerQuits = True;Win = False
            elif TheTile == "-f":
                FlagMode = not FlagMode
                print("FlagMode on" if FlagMode == True else "FlagMode off")
                RevealBoard()
            else:
                if TheTile in Minesweeper:
                    if Shown[TheTile] != True:
                        if Flagged[TheTile] != True:ChosenTile = TheTile;TileNoExists = False
                        else:
                            if FlagMode == False:
                                RevealBoard()    
                                print("Tile is Flagged! try another one." + " (" + TheTile + ")")
                            else:ChosenTile = TheTile;TileNoExists = False
                    else:
                        RevealBoard()
                        print("Tile already opened! try another one." + " (" + TheTile + ")")
                else:
                    RevealBoard()
                    print("Tile doesnt exist! try again." + " (" + TheTile + ")")
        if PlayerQuits == False:
            if FlagMode == False: RevealTile(ChosenTile)
            else: Flagged[ChosenTile] = not Flagged[ChosenTile]
            AllShown = True
            for xe in range(1,LimitX + 1):
                for ye in range(1,LimitY + 1):
                    Tile = str(xe) + ", " + str(ye)
                    if Shown[Tile] != True and Minesweeper[Tile] != "M": AllShown = False
                    if Shown[Tile] == True and Minesweeper[Tile] == "M": AllShown = False;GameActive = False
            if AllShown == True:Win = True;GameActive = False
            RevealBoard()
        else:
            subprocess.run('clear')
            for i in range(1,len((Printer := {1: "", 2: "You Quitted.", 3: ""})) + 1): print(Printer[i])
    EndMessage = "You win!" if Win == True else "You Lose."
    input(EndMessage + " Enter anything to continue:")
def Settings():
    global LimitX,LimitY,Mines,SafeStart
    subprocess.run('clear')
    for i in range(1,len((Printer := {1 : "", 2 : "TERMINAL SWEEPER", 3 : "", 4 : "-- SETTINGS --", 5 : "LimitX: " + str(LimitX), 6 : "LimitY: " + str(LimitY), 7 : "Mines: " + str(Mines), 8 : "SafeStart: " + str(SafeStart), 9 : "", 10: "-- PRESETS --", 11: "-ge: Easy Gamemode (TilesX = 10, TilesY = 10, Mines = 10)", 12: "-gi: Intermediate Gamemode (TilesX = 16, TilesY = 16, Mines = 40)", 13: "-gh: Expert Gamemode (TilesX = 30, TilesY = 16, Mines = 99)", 14: "-gm: Master Gamemode (TilesX = 50, TilesY = 50, Mines = 450)", 15: "-gl: Legend Gamemode (TilesX = 100, TilesY = 100, Mines = 2000)", 16: ""})) + 1): print(Printer[i])
    Option = input("Enter a Setting to Change, or Write -e to exit:")
    subprocess.run('clear')
    if Option in (SettingsDict := {"LimitX" : {"Text" : "LimitX: " + str(LimitX), "Type" : "Int", "Min" : 3, "Max" : 100}, "LimitY" : {"Text" : "LimitY: " + str(LimitY), "Type" : "Int", "Min" : 3, "Max" : 100}, "Mines" : {"Text" : "Mines: " + str(Mines), "Type" : "Int", "Min" : 1, "Max" : LimitX * LimitY}, "SafeStart" : {"Text" : "SafeStart: " + str(SafeStart), "Type" : "Bool"}}):
        for i in range(1,len((Printer := {1: "", 2: SettingsDict[Option]["Text"], 3: ""})) + 1): print(Printer[i])
        if SettingsDict[Option]["Type"] == "Int":
            Setting = input(f"Write a Number from {str(SettingsDict[Option]["Min"])} to {str(SettingsDict[Option]["Max"])}:")
            if Setting.isdigit():
                if int(Setting) >= SettingsDict[Option]["Min"] and int(Setting) <= SettingsDict[Option]["Max"]: globals()[Option] = int(Setting)
        elif SettingsDict[Option]["Type"] == "Bool":
            Setting = input("Write -t to Toggle this option.")
            if Setting == "-t":globals()[Option] = not globals()[Option]
    elif Option in (OptionsDict := {"-ge" : {"LimitX" : 10,"LimitY" : 10,"Mines" : 10},"-gi" : {"LimitX" : 16,"LimitY" : 16,"Mines" : 40},"-gh" : {"LimitX" : 30,"LimitY" : 16,"Mines" : 99},"-gm" : {"LimitX" : 50,"LimitY" : 50,"Mines" : 450},"-gl" : {"LimitX" : 100,"LimitY" : 100,"Mines" : 2000}}):
        for key, value in OptionsDict[Option].items():
            if key in globals(): globals()[key] = value
    if Mines >= LimitX * LimitY:Mines = LimitX * LimitY
    if Option != "-e": Settings()
def Controls():
    global LimitX,LimitY,Mines
    subprocess.run('clear')
    for i in range(1,len((Printer := {1: "", 2: "TERMINAL SWEEPER", 3: "", 4: "-- GAMEPLAY --", 5: "[X, Y]: Select Tile", 6: "-f: Toggle Flag mode", 7: "-q: Quit Game", 8: "[Enter]: Refresh board, yields error", 9: "", 10: "-- SETTINGS --", 11: "[Option] (Menu): Select option to change", 12: "[Preset] (Menu): Select Preset to set", 13: "-e (Menu): Exit", 14: "[Enter] (Menu): Refresh", 15: "[Valid Input] (Selection): Change Value to Input", 16: "[Enter] (Selection): Leave", 17: "", 18: "This is version 1.1, go to " + '\033[4mhttps://github.com/Tangramice/TerminalSweeper\033[0m' + " for more info", 19: ""})) + 1): print(Printer[i])
    Option = input("Enter to Exit, or write -l for attached links:")
    if Option == "-l":
        subprocess.run('clear')
        for i in range(1,len((Printer := {1: "", 2: "TERMINAL SWEEPER", 3: "", 4: "Official TerminalSweeper Github Page:" + '\033[4mhttps://github.com/Tangramice/TerminalSweeper\033[0m', 5: "", 6: "Enter to Exit:"})) + 1): print(Printer[i])
        Controls()
def Quit(IsCanceled):
    global Playing
    subprocess.run('clear')
    for i in range(1,len((Printer := {1: "", 2: "TERMINAL SWEEPER", 3: "Goodbye!", 4: "", 5: ("Dont use Ctrl+C next time! Use Q instead!" if IsCanceled == True else "-Open Source Project by TangramIce-")})) + 1): print(Printer[i])
    Playing = False
while Playing:
    subprocess.run('clear')
    for i in range(1,len((Printer := {1: "", 2: "TERMINAL SWEEPER", 3: "Hello!", 4: "", 5: "ENTER: Start Game", 6: "S: Settings", 7: "Q: Quit", 8: "C: Show Controls", 9: ""})) + 1): print(Printer[i])
    try:
        Option = input("Choose Option:")
        Quit(False) if str.upper(Option) == "Q" else Settings() if str.upper(Option) == "S" else Controls() if str.upper(Option) == "C" else Play()
    except KeyboardInterrupt: Quit(True)