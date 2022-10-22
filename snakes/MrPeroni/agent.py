import itertools

class Agent:
    def __init__(self, game_state):
        self.board = game_state["board"]
        self.grid = {(i,j): 0 for i,j in itertools.product(range(self.board["width"]), range(self.board["width"]))}
        # Cibo
        for food in self.board["food"]:
            self.grid[(food["x"],food["y"])] = 2
        # Avversari
        # for snake in self.board["snakes"]:
        #     if snake.
