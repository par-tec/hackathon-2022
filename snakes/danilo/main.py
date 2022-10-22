# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import pprint

FREE = ' '
FOOD = 'o'
WALL = '*'
SNAKE = '+'


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "danilo",  # TODO: Your Battlesnake Username
        "color": "#AA8833",  # TODO: Choose color
        "head": "bendr",  # TODO: Choose head
        "tail": "freckled",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def init_board(game_state: typing.Dict):
    # init board
    pprint.pprint(game_state)
    
    board = [[FREE for x in range(game_state['board']['width'] + 2)] for y in range(game_state['board']['height'] + 2)]
    
    for x in range(game_state['board']['width'] + 2):
        for y in range(game_state['board']['height'] + 2):
            if x == 0 or x == game_state['board']['width'] + 1 or y == 0 or y == game_state['board']['height'] + 1:
                board[x][y] = WALL
    
    for food in game_state['board']['food']:
        board[ food["x"] + 1 ][ food["y"] + 1 ] = FOOD

    for you in game_state['you']['body']:
        board[you["x"] + 1][you["y"] + 1] = SNAKE

    for snakes in game_state['board']['snakes']:
        for s in snakes['body']:
            board[s["x"] + 1][s["y"] + 1] = SNAKE

    return board

def can_move(direction, board, my_head):
    return look_at(direction, board, my_head, FOOD) or look_at(direction, board, my_head, FREE)

def check_food(direction, board, my_head):
    return look_at(direction, board, my_head, FOOD)


def look_at(direction, board, my_head, what):
    if direction == 'up':
        return board[ my_head["x"]][ my_head["y"] + 1 ] == what
    
    if direction == 'down':
        return board[ my_head["x"]][ my_head["y"] - 1 ] == what

    if direction == 'right':
        return board[ my_head["x"] + 1][ my_head["y"] ] == what
        
    if direction == 'left':
        return board[ my_head["x"] - 1][ my_head["y"] ] == what
    return False

def my_direction(game_state):

    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your neck
    my_neck["x"] = my_neck["x"] + 1
    my_neck["y"] = my_neck["y"] + 1
    
    if my_head['x'] == my_neck['x']:
        if my_head['y'] + 1 == my_neck['y']:
            print("direction: down")
            return 'down'
        if my_head['y'] - 1 == my_neck['y']:
            print("direction: up")
            return 'up'

    if my_head['y'] == my_neck['y']:
        if my_head['x'] + 1 == my_neck['x']:
            print("direction: left")
            return 'left'
        if my_head['x'] - 1 == my_neck['x']:
            print("direction: right")
            return 'right'
        
        
# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    
    board = init_board(game_state)
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_head["x"] = my_head["x"] + 1
    my_head["y"] = my_head["y"] + 1

    pprint.pprint(board)
    pprint.pprint(my_head)

    preferred_directions = ['up', 'right', 'down', 'left']


    my_actual_direction = my_direction(game_state)
    print("my actual direction: %s" % my_actual_direction)

    preferred_directions = [my_actual_direction] + preferred_directions
    
    for d in ['up', 'right', 'down', 'left']:
        if check_food(d, board, my_head):
            preferred_directions = [d] + preferred_directions
            print(f"FOOD found food!!!!")
            print(preferred_directions)


    for d in preferred_directions:
        if can_move(d, board, my_head):
            print(f"MOVE {game_state['turn']}: {d}")
            return {"move": d}

    return {"move": 'down'}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
