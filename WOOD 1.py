import sys
import math

# Begin Util Code
def log(x):
    print(x, file=sys.stderr)


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.item = NONE


class Customer:
    def __init__(self):
        self.item = NONE
        self.award = NONE

    def items(self):
        return self.item.split("-")


class Tile:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.item = NONE

    def parse_name(self):
        return self.name.split("-")

    def __repr__(self):
        return "Tile: " + str(self.x) + ", " + str(self.y)


class Step:
    def __init__(self, oven_content, oven_timer):
        self.oven_content = oven_content
        self.oven_timer = oven_timer


def make_step(game):  # updating state of all map
    turns_remaining = int(input())

    # PLAYERS INPUT
    # Gather and update player information
    player_x, player_y, player_item = input().split()
    player_x = int(player_x)
    player_y = int(player_y)
    game.updatePlayer(player_x, player_y, player_item)

    # Gather and update partner information
    partner_x, partner_y, partner_item = input().split()
    partner_x = int(partner_x)
    partner_y = int(partner_y)
    game.updatePartner(partner_x, partner_y, partner_item)

    # Gather and update table information
    for t in game.tiles:
        t.item = None
    num_tables_with_items = int(
        input())  # the number of tables in the kitchen that currently hold an item
    for i in range(num_tables_with_items):
        table_x, table_y, item = input().split()
        table_x = int(table_x)
        table_y = int(table_y)
        game.getTileByCoords(table_x, table_y).item = item

    # oven_contents
    oven_contents, oven_timer = input().split()
    oven_timer = int(oven_timer)
    num_customers = int(
        input())  # the number of customers currently waiting for food
    for i in range(num_customers):
        customer_item, customer_award = input().split()
        customer_award = int(customer_award)
        game.updateCustomer(customer_item, customer_award)

    return Step(oven_contents,
                oven_timer)  # for tracking separately oven state


def take_dish(game):  # first step - take dish for order
    dish_tile = None
    while True:
        if DISH not in game.player.item:
            make_step(game)
            game.use(game.getTileByName(DISHWASHER))
            if DISH in game.player.item:
                break
        else:
            break

    while True:
        if DISH in game.player.item:
            make_step(game)
            dish_tile = game.getTileByName(EMPTY_TABLE)
            game.use(dish_tile)
            if DISH not in game.player.item:
                break
        else:
            break

    return dish_tile


def check_dish_readiness(game, item):  # helping func for checking
    if game.getTileByItem(item) is not None:
        if NONE not in game.player.item:
            game.use(game.getTileByName(EMPTY_TABLE))
        return True
    return False
    # если блюдо есть, то кладем на клетку, если блюда нет, то его нет.


def ready_dish(game, dish, dish_tile):  # tile with ready dish on the DISH
    new_dish_tile = None
    while True:
        if DISH not in game.player.item:
            make_step(game)
            game.use(dish_tile)
        else:
            break

    while True:
        if dish not in game.player.item:
            make_step(game)
            game.use(game.getTileByItem(dish))
        else:
            break

    while True:
        if DISH in game.player.item:
            make_step(game)
            new_dish_tile = game.getTileByName(EMPTY_TABLE)
            game.use(new_dish_tile)
        else:
            break

    return new_dish_tile


def give_order(game, tile):
    while True:
        if DISH not in game.player.item:
            make_step(game)
            game.use(tile)
        else:
            break

    while True:
        if DISH in game.player.item:
            game.use(game.getTileByName(WINDOW))
        else:
            break


# RECEPIES
def chopped_strawberries(game):
    while True:
        make_step(game)
        if check_dish_readiness(game, CHOPPED_STRAWBERRIES):
            return
        if CHOPPED_STRAWBERRIES in game.player.item:
            game.use(game.getTileByName(EMPTY_TABLE))
            continue
        if STRAWBERRIES in game.player.item:
            game.use(game.getTileByName(CHOPPING_BOARD))
            continue
        if NONE in game.player.item:
            game.use(game.getTileByName(STRAWBERRIES_CRATE))
            continue


def croissant(game):
    while True:
        step_data = make_step(game)
        if check_dish_readiness(game, CROISSANT):
            return
        if CROISSANT in game.player.item:
            game.use(game.getTileByName(EMPTY_TABLE))
            continue
        if CROISSANT in step_data.oven_content:
            game.use(game.getTileByName(OVEN))
            continue
        if DOUGH in step_data.oven_content:
            game.wait()
            continue
        if DOUGH in game.player.item:
            game.use(game.getTileByName(OVEN))
            continue
        if NONE in game.player.item:
            game.use(game.getTileByName(DOUGH_CRATE))
            continue


def blueberries(game):
    while True:
        make_step(game)
        if check_dish_readiness(game, BLUEBERRIES):
            return


def ice_cream(game):
    while True:
        make_step(game)
        if check_dish_readiness(game, ICE_CREAM):
            return


# end of recepies

def cook(game, dish_list):  # main function
    new_tile = None
    tile = take_dish(game)  # take dish and memorise its location
    dish_list.remove("DISH")
    for dish in dish_list:  # check if recepy is in order
        log(dish)
        log(dish_list)
        if dish in recepies.keys():  # check if we know this recepy???
            recepies[dish](game)  # cook recepies
            new_tile = ready_dish(game, dish,
                                  tile)  # and gather it on one dish
    give_order(game, new_tile)  # give the ready order


# Cells
BLUEBERRIES_CRATE = "B"
ICE_CREAM_CRATE = "I"
STRAWBERRIES_CRATE = "S"
DOUGH_CRATE = "H"
CHOPPING_BOARD = "C"
OVEN = "O"
WINDOW = "W"
EMPTY_TABLE = "#"
DISHWASHER = "D"
FLOOR_CELL = "."

# Items
NONE = "NONE"
DISH = "DISH"
ICE_CREAM = "ICE_CREAM"
BLUEBERRIES = "BLUEBERRIES"
STRAWBERRIES = "STRAWBERRIES"
CHOPPED_STRAWBERRIES = "CHOPPED_STRAWBERRIES"
DOUGH = "DOUGH"
CROISSANT = "CROISSANT"

recepies = {
    CHOPPED_STRAWBERRIES: chopped_strawberries,
    CROISSANT: croissant,
    BLUEBERRIES: blueberries,
    ICE_CREAM: ice_cream}


class Game:
    def __init__(self):
        self.player = Player()
        self.partner = Player()
        self.customer = Customer()
        self.tiles = []

    def addTile(self, x, y, tileChar):
        if tileChar != '.':
            self.tiles.append(Tile(x, y, tileChar))

    def getTileByName(self, name):
        for t in self.tiles:
            if t.name == name:
                return t

        # If tile not found
        log("Error: Tile not found in function getTileByName")

    def getTileByItem(self, item):
        for t in self.tiles:
            if t.item == item:
                return t
        # return None

    def getTileByCoords(self, x, y):
        for t in self.tiles:
            if t.x == x and t.y == y:
                return t

        # If tile not found
        log("Error: Tile not found in function getTileByCoords")

    def updatePlayer(self, x, y, item):
        self.player.x = x
        self.player.y = y
        self.player.item = item

    def updatePartner(self, x, y, item):
        self.partner.x = x
        self.partner.y = y
        self.partner.item = item

    def updateCustomer(self, item, award):
        self.customer.item = item
        self.customer.award = award

    def use(self, tile):
        print("USE", tile.x, tile.y, "; Python Starter AI")

    def move(self, tile):
        print("MOVE", tile.x, tile.y)

    def wait(self):
        print("WAIT")


# End Util code

# Begin game code
game = Game()

# ALL CUSTOMERS INPUT
num_all_customers = int(input())
for i in range(num_all_customers):
    customer_item, customer_award = input().split()
    customer_award = int(customer_award)

# KITCHEN INPUT
for y in range(7):
    kitchen_line = input()
    for x, tileChar in enumerate(kitchen_line):
        game.addTile(x, y, tileChar)

# items_list = []
make_step(game)  # first step while filling map
game.wait()  # вот тут мы ждем первый ход, хотя вообще-то мы уже можем двигаться
# game loop
while True:
    cook(game, game.customer.items())  # main func