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
from pprint import pprint

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "MrPeroni",  # TODO: Your Battlesnake Username
        "color": "#297516",  # TODO: Choose color
        "head": "safe",  # TODO: Choose head
        "tail": "freckled",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    from agent import Agent
    agg = Agent(game_state)

    next_step = agg.compute_step()
    if next_step != None:
        print("QAU")
        x,y = next_step
        print(f"{x},{y}")
        print(my_head["x"], my_head["y"])
        if x == my_head["x"] + 1:
            return {"move": "right"}
        elif x == my_head["x"] - 1:
            return {"move": "left"}
        elif y == my_head["y"] + 1:
            return {"move": "up"}
        elif y == my_head["y"] - 1:
            return {"move": "down"}
        else:
            print("CAZZOOOOOOOOOOOOOOO!!!!!!!!111111")
            return {"move": "left"}

    else:
        print("NO QAU")

        # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
        board_width = game_state['board']['width']
        board_height = game_state['board']['height']

        if my_head["x"] == 0: # don't go left
            is_move_safe["left"] = False
        if my_head["x"] == board_width-1: # don't go right
            is_move_safe["right"] = False

        if my_head["y"] == 0: # don't go down
            is_move_safe["down"] = False
        if my_head["y"] == board_height-1: # don't go up
            is_move_safe["up"] = False
        
        # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
        my_body = game_state['you']['body']

        def hit_itself(x, y, body) -> bool:
            for cell in body:
                if x == cell["x"] and y == cell["y"]:
                    return True
            return False
        
        is_move_safe["up"] = (not hit_itself(my_head["x"], my_head["y"]+1, my_body)) and is_move_safe["up"] 
        is_move_safe["down"] = (not hit_itself(my_head["x"], my_head["y"]-1, my_body)) and is_move_safe["down"] 
        is_move_safe["left"] = (not hit_itself(my_head["x"]-1, my_head["y"], my_body)) and is_move_safe["left"] 
        is_move_safe["right"] = (not hit_itself(my_head["x"]+1, my_head["y"], my_body)) and is_move_safe["right"] 

        # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
        opponents = game_state['board']['snakes']
        
        def hit_opponent(x, y, opponent) -> bool:
            return hit_itself(x, y, opponent["body"])

        for opponent in opponents:
            if opponent["id"] != game_state["you"]["id"]:
                is_move_safe["up"] = (not hit_opponent(my_head["x"], my_head["y"]+1, opponent)) and is_move_safe["up"] 
                is_move_safe["down"] = (not hit_opponent(my_head["x"], my_head["y"]-1, opponent)) and is_move_safe["down"] 
                is_move_safe["left"] = (not hit_opponent(my_head["x"]-1, my_head["y"], opponent)) and is_move_safe["left"] 
                is_move_safe["right"] = (not hit_opponent(my_head["x"]+1, my_head["y"], opponent)) and is_move_safe["right"]

        # Are there any safe moves left?
        safe_moves = []
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)

        if len(safe_moves) == 0:
            print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
            return {"move": "down"}

        # Choose a random move from the safe ones
        next_move = random.choice(safe_moves)

        # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
        # food = game_state['board']['food']

        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})