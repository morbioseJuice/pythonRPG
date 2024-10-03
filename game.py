import random
import os

"""
Copy this to use in Command Prompt
"C:/Program Files/Python310/python.exe" "c:/Users/28wbriggs/OneDrive - Davis School District/Non-School Related/Coding/Python/game.py"
"""

game = 1 # Starts the game on the menu

curwpn = 0 # The weapon you are using (pea shooter)
kills = 0
dmgdealt = 0
mhealth = 10
health = 10
itemcount = 1
coins = 0

weapons = [ #0: name, 1:dmgmin 2: dmgmax  3: obtained? 4: description 5: effect
    ["Pea shooter", 1, 2, True, "It... might do something? Damage: 1-2"], #peashooter 0
    ["-NOT UNLOCKED-", 2, 2, False, "Very old. Damage: 2"], #oldglock 1
    ["-NOT UNLOCKED-", 2, 3, False, "Not bad. Damage: 2-3"], #Basic Rifle 2
    ["-NOT UNLOCKED-", 2, 5, False, "It's explosive. Damage: 2-5"], #Bomb 3
    ["-NOT UNLOCKED-", 8, 12, True, "BOOM. Damage: 8-12"], #BIG Bomb 4 
    ["-NOT UNLOCKED-", 0, 3, False, "Does damage... most of the time? Damage: 0-3"], #stick 5
]

def Attack(e): # The Attack function
    e.taken = (random.randint(weapons[curwpn][1], weapons[curwpn][2]) - e.defense) # Calculates dealt damage
    if (e.taken < 0): # Stops healing
        e.taken = 0
    e.health -= e.taken
    if (e.health < 0): # Stops enemy from being over-killed
        e.taken -= abs(e.health)
        e.health = 0
    else:
        e.given = random.randint(e.dmgmin, e.dmgmax) # Damage dealt by enemy
    return e

def clear(): # Clears the terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def ChooseEnemy(): # Selects the enemy that the player will fight
    num = random.randint(1, 100)
    
    if num <= 70: # Slime 70%
        return ["slime", 3, 0, 1, 1]
    elif num <= 88: # Zombie 18%
        return ["zombie", 5, 1, 1, 3]
    elif num >= 89: # Boss 12%
        num = random.randint(1, 2)    
        if num == 1: # Exploder
            return ["exploder", 10, 1, 1, 4]
        elif num == 2: # Imploder
            return ["imploder", 15, 1, 2, 4]
        
def CheckLoot(type): # Checks what loot player receives
    # Any
    global itemcount
    if random.randint(1, 5) == 5 and weapons[1][3] == False:
        weapons[1][0] = "Old Glock"
        weapons[1][3] = True
        itemcount += 1
        print(f"You found a {weapons[1][0]}")
    
    # Zombie
    if random.randint(1, 5) == 5 and weapons[2][3] == False and type == "zombie":
        weapons[2][0] = "Basic Rifle"
        weapons[2][3] = True
        itemcount += 1
        print(f"You found a {weapons[2][0]}")
    
    # Exploder
    if random.randint(1, 1) == 1 and weapons[3][3] == False and type == "exploder":
        weapons[3][0] = "Bomb"
        weapons[3][3] = True
        itemcount += 1
        print(f"You found a {weapons[3][0]}")
    
    # Imploder
    if random.randint(1, 1) == 1 and weapons[4][3] == False and type == "imploder":
        weapons[4][0] = "BIG Bomb"
        weapons[4][3] = True
        itemcount += 1
        print(f"You found a {weapons[4][0]}")
                
class Enemy: # The enemy class
    def __init__(self, type, health, defense, dmgmin, dmgmax):
        self.health = health
        self.defense = defense
        self.type = type
        self.taken = 0
        self.given = 0
        self.dmgmin = dmgmin
        self.dmgmax = dmgmax

e1 = Enemy("slime", 0, 0, 1, 1) # This enemy will never appear (just declaring)

while True: # Repeats forever
    clear()
    
    print(f"Your Health: {health} --- Enemy Health: {e1.health} --- Damage Given: {e1.taken} --- COINS: {coins}") # Displays stats
    
    if   game == 1: # Menu
        print("MENU\n1) Play\n2) Change Weapon\n3) Statistics\n4) Shop\n5) Quit")
        opt = input("select")
        
        if opt == "1" or opt == "y" or opt == "": # Fight
            game = 2 # Changes game mode   
            chunk = ChooseEnemy() # Selects the enemy
            health = mhealth # Gives your health back
            e1 = Enemy(chunk[0], chunk[1], chunk[2], chunk[3], chunk[4])
        if opt == "2": # Weapon Select
            print(f"CHOOSE WEAPON\n")
            for i in range(len(weapons)): # shows the options efficiently
                print(f"{i}) {weapons[i][0]}")

            opt = input("select") # the number inpout
            while opt.isdigit() == False: # stops errors from happening when input is not a number
                opt = input("That is invalid. Pick again.")
            opt = int(opt) # concatenates the input

            if weapons[opt][3] == True: # checks if you have the item, then sets the weapon
                print(weapons[opt][4]); input()
                curwpn = opt
            else:
                print("You don't have that weapon"); input()
        if opt == "3": # Stats
            game = 3 #stats
        if opt == "4": # Shop
            game = 4    
        if opt == "5": # Quit
            exit()
    elif game == 2: # Fight 
        ans = input(f"Would you like to fight the {e1.type}?") # Why wouldn't you?
        if (ans == "yes" or ans == "y" or ans == ""):
            e1 = Attack(e1) # Attacks the enemy
            health -= e1.given # Takes damage
            dmgdealt += e1.taken # Changes stat
            
            if(health < 0): # Player Dies
                health = mhealth 
                game = 1
            
            if(e1.health == 0): # Enemy Dies
               
                print(f"The {e1.type} is dead. You win!")
                kills += 1 # Increase kill count
                coins += random.randint(1, 2) # Gives coins

                CheckLoot(e1.type) # Sees if you get loot

                input()

                game = 1
        elif (ans == "no"):
            game = 1
    elif game == 3: # Stats
        print(f"Kills: {kills}\nWeapons: {itemcount}/{len(weapons)}\nDamage dealt: {dmgdealt}"); input()
        game = 1
    elif game == 4: # Shop
        print("SHOP\n1) Stick (50c)\n2) +2 health  (100c)\n3) Quit")
        opt = input("select")
        if opt == "1" and coins >= 50 and weapons[5][3] == False:
            coins -= 50
            weapons[5][0] = "Stick"
            weapons[5][3] = True
            itemcount += 1
        if opt == "2":
            mhealth += 2
            coins -= 100
        if opt == "3":
            game = 1

'''
To do:

Items:

Add effects (poison, freeze)
Add health potions

Enemies:

Give slime a drop
Add a ton of random enemies
Sort enemies by regular, mini-boss, and boss
'''