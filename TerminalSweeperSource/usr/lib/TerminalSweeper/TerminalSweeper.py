#!/usr/bin/env python3

import random
import subprocess

Playing = True

LimitX = 10
LimitY = 10
Mines = 10
SafeStart = True

def Play():
    global LimitX,LimitY,Mines,SafeStart
    Minesweeper = {}
    Shown = {}
    Flagged = {}
    GameActive = True
    Win = False
    FlagMode = False
    PlayerQuits = False
    EndMessage = ""
    Colors = {"0": '3', "1": '94', "2": '32', "3": '91', "4": '34', "5": '31', "6": '36', "7": '30', "8": '37', "M": '41', "X": '0', "F": '7'}

    def RevealTile(STile):
        if Shown[STile] == False:
            posi = STile.find(", ")
            Shown[STile] = True
            if Minesweeper[STile] == 0:
                for xo in range(int(STile[0:posi])-1,int(STile[0:posi])+2):
                    for yo in range(int(STile[posi+2:])-1,int(STile[posi+2:])+2):
                        ChainedTile = str(xo) + ", " + str(yo)
                        if ChainedTile in Minesweeper:
                            RevealTile(ChainedTile)

    def RevealBoard():
        subprocess.run('clear')
        for yp in range(1,LimitY + 1):
            Row = ""
            for xp in range(1,LimitX + 1):
                Tiler = str(xp) + ", " + str(yp)
                Emit = str(Minesweeper[Tiler])
                if Shown[Tiler] == False:
                    Emit = "X"
                if Flagged[Tiler] == True:
                    Emit = "F"
                if GameActive == False and Minesweeper[Tiler] == "M":
                    if Win == True:
                        Emit = "F"
                    else:
                        Emit = "M"
                Row += '\033[' + Colors[Emit] +'m'+ Emit + '\033[0m' + " "
            print(Row)
        print("")
            
    for x in range(1,LimitX + 1):
        for y in range(1,LimitY + 1):
            Tile = str(x) + ", " + str(y)
            Minesweeper[Tile] = 0
            Shown[Tile] = False
            Flagged[Tile] = False

    RevealBoard()

    TileNoExists = True
    ChosenTile = ""
    while TileNoExists:
        TheTile = input("Enter A Tile (X, Y):" )
        if TheTile in Minesweeper:
            ChosenTile = TheTile
            TileNoExists = False
        else:
            print("Tile doesnt exist! try again.")
    NoNoSquares = {}
    pos = ChosenTile.find(", ")
    
    for xo in range(int(ChosenTile[0:pos])-1,int(ChosenTile[0:pos])+2):
        for yo in range(int(ChosenTile[pos+2:])-1,int(ChosenTile[pos+2:])+2):
                Tiled = str(xo) + ", " + str(yo)
                if Tiled in Minesweeper:
                    NoNoSquares[Tiled] = True
    
    if SafeStart == False:
        NoNoSquares = {}
    
    if Mines >= LimitX * LimitY - len(NoNoSquares):
        NoNoSquares = {}

    if Mines >= LimitX * LimitY:
        Mines = LimitX * LimitY

    for r in range(1,Mines + 1):
        xa = 0
        ya = 0
        AlreadyMine = True
        while AlreadyMine:
            xa = random.randint(1,LimitX)
            ya = random.randint(1,LimitY)
            if Minesweeper[str(xa) + ", " + str(ya)] != "M":
                if not str(xa) + ", " + str(ya) in NoNoSquares:
                    AlreadyMine = False
        Mine = str(xa) + ", " + str(ya)
        Minesweeper[Mine] = "M"
        for xi in range(xa-1,xa+2):
            for yi in range(ya-1,ya+2):
                Tiled = str(xi) + ", " + str(yi)
                if Tiled in Minesweeper:
                    if Minesweeper[Tiled] != "M":
                        Minesweeper[Tiled] += 1

    RevealTile(ChosenTile)

    AllShown = True
    for xe in range(1,LimitX + 1):
        for ye in range(1,LimitY + 1):
            Tile = str(xe) + ", " + str(ye)
            if Shown[Tile] != True and Minesweeper[Tile] != "M":
                AllShown = False
            if Shown[Tile] == True and Minesweeper[Tile] == "M":
                AllShown = False
                GameActive = False
        
    if AllShown == True:
        Win = True
        GameActive = False

    RevealBoard()

    while GameActive == True:
        TileNoExists = True
        ChosenTile = ""
        while TileNoExists:
            Input = "Enter A Tile to Open (X, Y) [Write -f to Toggle on flag mode or -q to Quit]:"
            if FlagMode == True:
                Input = "Enter A Tile to Flag (X, Y) [Write -f to Toggle off flag mode or -q to Quit]:"
            TheTile = input(Input)
            if TheTile == "-q":
                GameActive = False
                TileNoExists = False
                PlayerQuits = True
                Win = False
            elif TheTile == "-f":
                FlagMode = not FlagMode
                if FlagMode == True:
                    RevealBoard()
                    print("FlagMode on")
                else:
                    RevealBoard()
                    print("FlagMode off")
            else:
                if TheTile in Minesweeper:
                    if Shown[TheTile] != True:
                        if Flagged[TheTile] != True:
                            ChosenTile = TheTile
                            TileNoExists = False
                        else:
                            if FlagMode == False:
                                RevealBoard()    
                                print("Tile is Flagged! try another one." + " (" + TheTile + ")")
                            else:
                                ChosenTile = TheTile
                                TileNoExists = False
                    else:
                        RevealBoard()
                        print("Tile already opened! try another one." + " (" + TheTile + ")")
                else:
                    RevealBoard()
                    print("Tile doesnt exist! try again." + " (" + TheTile + ")")

        if PlayerQuits == False:
            if FlagMode == False:
                RevealTile(ChosenTile)
            else:
                Flagged[ChosenTile] = not Flagged[ChosenTile]
     
            AllShown = True
            for xe in range(1,LimitX + 1):
                for ye in range(1,LimitY + 1):
                    Tile = str(xe) + ", " + str(ye)
                    if Shown[Tile] != True and Minesweeper[Tile] != "M":
                        AllShown = False
                    if Shown[Tile] == True and Minesweeper[Tile] == "M":
                        AllShown = False
                        GameActive = False
        
            if AllShown == True:
                Win = True
                GameActive = False
        
            RevealBoard()
        else:
            subprocess.run('clear')
            print("")
            print("You Quitted.")
            print("")

    if Win == True:
        EndMessage = "You win!"
    else:
        EndMessage = "You Lose."

    input(EndMessage + " Enter anything to continue:")

def Settings():
    global LimitX,LimitY,Mines,SafeStart
    subprocess.run('clear')
    print("")
    print("TERMINAL SWEEPER")
    print("")
    print("-- SETTINGS --")
    print("TilesX: " + str(LimitX))
    print("TilesY: " + str(LimitY))
    print("Mines: " + str(Mines))
    print("Always Safe Start: " + str(SafeStart))
    print("")
    print("-- PRESETS --")
    print("-ge: Easy Gamemode (TilesX = 10, TilesY = 10, Mines = 10)")
    print("-gi: Intermediate Gamemode (TilesX = 16, TilesY = 16, Mines = 40)")
    print("-gh: Expert Gamemode (TilesX = 30, TilesY = 16, Mines = 99)")
    print("-gm: Master Gamemode (TilesX = 50, TilesY = 50, Mines = 450)")
    print("-gl: Legend Gamemode (TilesX = 100, TilesY = 100, Mines = 2000)")
    print("")
    Option = input("Enter a Setting to Change, or Write -e to exit:")

    if Option == "TilesX":
        subprocess.run('clear')
        print("")
        print("TilesX: " + str(LimitX))
        print("")
        Setting = input("Write a Number from 3 to 100:")
        if Setting.isdigit():
            if int(Setting) >= 3 and int(Setting) <= 100:
                LimitX = int(Setting)
        if Mines >= LimitX * LimitY:
            Mines = LimitX * LimitY
        Settings()
    elif Option == "TilesY":
        subprocess.run('clear')
        print("")
        print("TilesY: " + str(LimitY))
        print("")
        Setting = input("Write a Number from 3 to 100:")
        if Setting.isdigit():
            if int(Setting) >= 3 and int(Setting) <= 100:
                LimitY = int(Setting)
        if Mines >= LimitX * LimitY:
            Mines = LimitX * LimitY
        Settings()
    elif Option == "Mines":
        subprocess.run('clear')
        print("")
        print("Mines: " + str(Mines))
        print("")
        Setting = input("Write a Number from 1 to " + str(LimitX * LimitY) + ":")
        if Setting.isdigit():
            if int(Setting) >= 1 and int(Setting) <= LimitX * LimitY:
                Mines = int(Setting)
        Settings()
    elif Option == "Always Safe Start":
        subprocess.run('clear')
        print("")
        print("Always Safe Start: " + str(SafeStart))
        print("")
        Setting = input("Write -t to Toggle this option.")
        if Setting == "-t":
            SafeStart = not SafeStart
        Settings()
    elif Option == "-ge":
        LimitX = 10
        LimitY = 10
        Mines = 10
        Settings()
    elif Option == "-gi":
        LimitX = 16
        LimitY = 16
        Mines = 40
        Settings()
    elif Option == "-gh":
        LimitX = 30
        LimitY = 16
        Mines = 99
        Settings()
    elif Option == "-gm":
        LimitX = 50
        LimitY = 50
        Mines = 450
        Settings()
    elif Option == "-gl":
        LimitX = 100
        LimitY = 100
        Mines = 2000
        Settings()
    elif Option != "-e":
        Settings()
    
def Controls():
    global LimitX,LimitY,Mines
    subprocess.run('clear')
    print("")
    print("TERMINAL SWEEPER")
    print("")
    print("-- GAMEPLAY --")
    print("[X, Y]: Select Tile")
    print("-f: Toggle Flag mode")
    print("-q: Quit Game")
    print("[Enter]: Refresh board, yields error")
    print("")
    print("-- SETTINGS --")
    print("[Option] (Menu): Select option to change")
    print("[Preset] (Menu): Select Preset to set")
    print("-e (Menu): Exit")
    print("[Enter] (Menu): Refresh")
    print("[Valid Input] (Selection): Change Value to Input")
    print("[Enter] (Selection): Leave")
    print("")
    print("This is version 1.1, go to " + '\033[4mhttps://github.com/Tangramice/TerminalSweeper\033[0m' + " for more info")
    print("")
    Option = input("Enter to Exit, or write -l for attached links:")

    if Option == "-l":
        subprocess.run('clear')
        print("")
        print("TERMINAL SWEEPER")
        print("")
        print("Official TerminalSweeper Github Page:" + '\033[4mhttps://github.com/Tangramice/TerminalSweeper\033[0m')
        print("")
        input("Enter to Exit:")
        Controls()
        

def Quit():
    global Playing
    subprocess.run('clear')
    print("")
    print("TERMINAL SWEEPER")
    print("Goodbye!")
    print("")
    print("-Open Source Project by TangramIce-")
    Playing = False

while Playing:
    subprocess.run('clear')
    print("")
    print("TERMINAL SWEEPER")
    print("Hello!")
    print("")
    print("ENTER: Start Game")
    print("S: Settings")
    print("Q: Quit")
    print("C: Show Controls")
    print("")
    Option = input("Choose Option:")

    if str.upper(Option) == "Q":
        Quit()
    elif str.upper(Option) == "S":
        Settings()
    elif str.upper(Option) == "C":
        Controls()
    else:
        Play()
