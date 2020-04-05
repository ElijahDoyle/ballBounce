import random
import time
import sys


# the Character class acts as the base for the player, with methods like attack, displayInventory, etc.
class Character:
    def __init__(self, name):
        self.name = name
        self.health = 20  # current amount of health
        self.maxHealth = 20  # max amount of health
        self.armor = ["Hat",
                      2]  # in self.armor and self.weapon, the first index in the list is the Weapon itself, and the second is the value
        self.weapon = ["Fists", 5]
        self.attackValue = self.weapon[1]  # equals the value of the weapon
        self.defenseValue = self.armor[1]  # equals the value of the armor
        self.isFleeing = False  # the state in which the player is fleeing or not (initially set to False
        self.inventory = {
            "Gold": 0,  # gold to potentially be used in a shop
            "Weapon": self.weapon[0],  # the name of the weapon equipped
            "Armor": self.armor[0],  # the name of the armor equipped
            "Stick": "Just a stick",  # just a stick
            "Health Potion": "Heals 5 health"
        }
        self.spells = {}  # dictionary of spells known by the player with associated damage values
        self.defending = False
        self.addedDefense = 0 \
 \
            # the displayInventory method does just that, prints out all items with their amount/description

    def displayInventory(self):
        print("")
        for key in self.inventory:
            print(key, " : ", self.inventory[key])

    # the addInventory adds an item to the inventory and a value to the new key
    def addInventory(self, newItem, newValue):
        self.inventory[newItem] = newValue

    # the attack method does a random amount of damgage based upon attack, and subracts that damage from the enemy Health
    def attack(self, enemyHealth, enemyDefense):
        damage = random.randint(self.attackValue - 5, self.attackValue + 5)  # this allows for variation in attacks
        print("")
        time.sleep(1)
        print("%s attacked with their %s" % (self.name, self.weapon[0]))
        print("")
        damage = damage - enemyDefense
        if damage <= 0:  # this if statement ensures you don't do negative damage
            damage = 0
            time.sleep(1)
            print("The enemy blocked the attack!")
            print("")
        elif damage == self.attackValue + 5:  # an attack is a 'critical hit' when it does the max amount of damage
            time.sleep(1)
            print("Critical Hit!")
            print("")
        time.sleep(1)
        enemyHealth = enemyHealth - (damage)  # this actually does the damage
        if enemyHealth < 0:  # this if statement ensures an enemy doesn't have negative health
            enemyHealth = 0
        print("%s damage done!" % (damage))
        time.sleep(1)
        return enemyHealth

    # the flee method just gives the player a chance to escape
    def flee(self, enemyName):
        chanceOfEscape = random.randint(0, 5)
        time.sleep(1)
        if chanceOfEscape == 1:
            print("")
            print("Got away safely!")
            self.isFleeing = True
        else:
            print("")
            print("The %s blocked the way!" % (enemyName))
        time.sleep(1)

    # the defend method creates a value that will be subracted from the enemy's attack for 1 turn
    def defend(self):
        addedDefense = random.randint(1, 5)
        return addedDefense

    # the magic method will do something when i work it out
    def magic(self):
        if len(self.spells) > 0:
            return True
        else:
            print("")
            time.sleep(1)
            print(self.name + " doesn't know any spells yet!")
            time.sleep(3)
            print("")
            return False
                    # TODO : FIGURE THIS OUtT
    # this allows players to use an item from their inventory
    def useItem(self):
        self.displayInventory()
        print("")
        print("If you want to choose a different action type 'exit'.")
        isValid = False
        while not isValid:
            print("")
            choice = (input("Which item would you like to use? ")).lower()
            print("")
            time.sleep(1)
            if choice == "gold":
                print("What are you going to do, pay him off?")
                print("")
                time.sleep(3)
                print("Choose another Item...")
                isValid = False
            elif choice == "weapon":
                print("Go back and select attack")
                print("")
                time.sleep(3)
                print("Choose another Item...")
                isValid = False
            elif choice == "armor":
                print("Go back and select defend")
                print("")
                time.sleep(3)
                print("Choose another Item...")
                isValid = False
            elif choice == "stick":
                print("This is a stick...")
                time.sleep(3)
                print("What are you going to do with a stick?")
                print("")
                time.sleep(3)
                print("Choose another Item...")
                isValid = False
            elif choice == "health potion":
                print(self.name + " used a health potion!")
                print("")
                time.sleep(3)
                hlthGained = self.maxHealth - self.health
                if hlthGained > 5:
                    hlthgained = 5
                print("+%s health!" % (hlthGained))
                print("")
                self.health += 5
                if self.health > 20:
                    self.health = 20
                    time.sleep(2)
                print("Player Health: ", self.health, " / ", self.maxHealth)
                del self.inventory["Health Potion"]
                isValid = True
                break
            elif choice == ('exit'):
                isValid = True
                return False
                break

            else:
                print("That is not in your inventory")
                time.sleep(2)
                continue


# This is the 'Enemy' class; it is a blueprint for any potential enemies the player may fight
class Enemy:
    def __init__(self, name, health, maxHealth, attackValue, defenseValue):
        self.name = name
        self.health = health
        self.maxHealth = maxHealth
        self.attackValue = attackValue
        self.defenseValue = defenseValue

    # the attack method does a random amount of damgage based upon attack, and subracts that damage from the enemy(the player's) Health
    def attack(self, playerDefenseValue, playerHealth, playerName):
        damage = random.randint(self.attackValue - 5, self.attackValue + 5)
        print("")
        time.sleep(1)
        print("The %s is attacking!" % (self.name))
        damage = damage - playerDefenseValue

        print("")
        if damage <= 0:  # ensures no negative damage
            damage = 0
            time.sleep(1)
            print("%s blocked the attack!" % (playerName))
            print("")
        elif damage == self.attackValue + 5:  # critical hit if the max damage is done
            time.sleep(1)
            print("Critical Hit!")
            print("")
        playerHealth = playerHealth - (damage)
        if playerHealth < 0:
            playerHealth = 0
        time.sleep(2)
        print("%s damage done!" % (damage))
        time.sleep(1)
        return playerHealth


# this function displays the battle menu
def displayBattleMenu():
    print("")
    print("-----------------------------")
    print("| Battle Menu:              |")
    print("|---------------------------|")
    print("|1.Attack     2.Use Item    |")
    print("|                           |")
    print("|3.Flee       4.Defend      |")
    print("|                           |")
    print("|5.Magic      6.Dance       |")
    print("-----------------------------")


# the selectBattleOption function gets user input and interprets the battle option
def selectBattleOption(PLAYER, ENEMY):
    validChoice = False
    if PLAYER.defending == True:
        PLAYER.defenseValue -= PLAYER.addedDefense
        PLAYER.defending = False
        PLAYER.addedDefense = 0

    while not validChoice:
        displayBattleMenu()
        print("")
        selectedOption = (
            input("Type the name of the action you wish to perform: ")).lower()  # the .lower allows for caps. variation

        if selectedOption == "attack":
            validChoice = True
            ENEMY.health = PLAYER.attack(ENEMY.health, ENEMY.defenseValue)  # the player attacks the enemy
            break
        elif selectedOption == "use item":
            validChoice = True

            if PLAYER.useItem() is False:
                validChoice = False
                continue
            else:
                break
        elif selectedOption == "flee":
            validChoice = True
            PLAYER.flee(ENEMY.name)  # there is a chance of fleeing.
            break
        elif selectedOption == "defend":
            validChoice = True
            PLAYER.addedDefense = PLAYER.defend()  # gives an added defense value to be used in the battle
            PLAYER.defenseValue += PLAYER.addedDefense
            PLAYER.defending = True
            print("")
            print("%s is defending..." % (PLAYER.name))
            time.sleep(2)
            break
        elif selectedOption == "magic":
            validChoice = PLAYER.magic()
        #    PLAYER.magic()  # does the magic stuff from the player class
          #  break
        elif selectedOption == "dance":
            print("")
            print("%s dances awkwardly..." % (PLAYER.name))  # just a fun lil thing
            time.sleep(2)
            validChoice = False
            continue
        else:  # This allows for error on the user's part
            print("")
            print("Thats not an option silly!")
            time.sleep(2)
            validChoice = False
            continue


player = Character("Test Character")
enemy = Enemy("skeleton", 20, 20, 2, 1)

# the isDead function basically returns true if something is dead
def isDead(Object):
    if Object.health <= 0:
        return True
    else:
        return False



# test battle stuff
def simpleBattle(player, enemy):
    while not player.isFleeing:
        selectBattleOption(player, enemy)
        if player.isFleeing == True:
            print("")
            time.sleep(3)
            break
        elif isDead(enemy):
            print("")
            time.sleep(3)
            print("ENEMY DEFEATED")
            time.sleep(3)
            break
        print("")
        print("Enemy Health: ", enemy.health, " / ", enemy.maxHealth)
        time.sleep(3)
        player.health = enemy.attack(player.defenseValue, player.health, player.name)
        print("")
        print("Player Health: ", player.health, " / ", player.maxHealth)
        if isDead(player):
            print("")
            print(player.name + "has been defeated...")
            time.sleep(3)
            print("")
            print("Press enter to quit")
            cont = input("")
            sys.quit()

        time.sleep(3)
simpleBattle(player,enemy)


