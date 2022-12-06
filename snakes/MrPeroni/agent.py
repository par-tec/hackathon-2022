import itertools
import networkx as nx
import math
import numpy as np

class Agent:
    def __init__(self, game_state):
        self.head = game_state["you"]["head"]
        self.board = game_state["board"]

        self.grid = {(i,j): 0 for i,j in itertools.product(range(self.board["width"]), range(self.board["height"]))}
        for snake in self.board["snakes"]:
            for pox in snake["body"]:
                self.grid[(pox["x"], pox["y"])] = 1

        # Togli la testa
        self.grid[(game_state["you"]["head"]["x"], game_state["you"]["head"]["y"])] = 0

        self.graph_grid = nx.grid_2d_graph(range(self.board["width"]), range(self.board["height"]))
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
        """
            Reuturns a list of food points ordered by the distance from the center of the board.
        """
        return sorted(
            self.board["food"],
            key=lambda p: math.dist(
                (p["x"], p["y"]),
                (self.board["width"]/2, self.board["height"]/2)
            )
        )

    def compute_step(self):
        """
            Compute the next step of the snake.
        """

        # Compute the Shortest Path Tree
        spt = nx.shortest_path(self.graph_grid, (self.head["x"], self.head["y"]))

        # If there is a food point on the board
        if len(self.board["food"]) != 0:

            # Get the most central food point
            for food_point in self.scores(): # euristica
                i, j = food_point["x"], food_point["y"]
                target_point = (i,j)

                # If the target point is reachable from the head
                if target_point in spt.keys():
                    # Get the next step
                    return spt[target_point][1]
        
        # If there is no food point on the board
        # or any food point is not reachable from the head
        return None