import itertools
import networkx as nx
import math
import numpy as np
from random import random

class Agent:
    def __init__(self, game_state):
        self.p = 0.75
        self.h = game_state["you"]["health"]
        self.head = game_state["you"]["head"]
        self.board = game_state["board"]

        self.grid = {(i,j): 0 for i,j in itertools.product(range(self.board["width"]), range(self.board["width"]))}
        
        # # Cibo
        # for food in self.board["food"]:
        #     self.grid[(food["x"],food["y"])] = 2

        # Corpo dei serpenti (compreso il mio)
        for snake in self.board["snakes"]:
            for pox in snake["body"]:
                self.grid[(pox["x"], pox["y"])] = 1

        # Togli la testa
        self.grid[(game_state["you"]["head"]["x"], game_state["you"]["head"]["y"])] = 0
        
        self.graph_grid = nx.grid_2d_graph(range(self.board["width"]), range(self.board["width"]))

        for i, j in self.grid.keys():
            if self.grid[i,j] == 1:
                self.graph_grid.remove_node((i,j))

    @np.deprecate
    def get_nearest_food(self):
        return self.board["food"][
            np.argmin( 
                map(lambda pox: math.dist(self.head, pox), self.board["food"])
            )
        ]
    
    def scores(self):
        return sorted(
            self.board["food"],
            key=lambda p: math.dist(
                (p["x"], p["y"]),
                (self.board["width"]/2, self.board["height"]/2)
            )
        )

    def compute_step(self):
        spt = nx.shortest_path(self.graph_grid, (self.head["x"], self.head["y"]))

        if len(self.board["food"]) != 0:
            # foods = self.scores() if random() <= 2/6 else self.board["food"]
            for food_point in self.scores(): # euristica
                i, j = food_point["x"], food_point["y"]
                target_point = (i,j)

                if target_point in spt.keys():
                    return spt[target_point][1]
        return None