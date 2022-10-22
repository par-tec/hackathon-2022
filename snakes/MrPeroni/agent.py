import itertools

class Agent:
    def __init__(self, game_state):
        self.board = game_state["board"]
        self.grid = {(i,j): 0 for i,j in itertools.product(range(self.board["width"]), range(self.board["width"]))}
        # Cibo
        for food in self.board["food"]:
            self.grid[(food["x"],food["y"])] = 2
        # Corpo dei serpenti (compreso il mio)
        for snake in self.board["snakes"]:
            for pox in snake["body"]:
                self.grid[(pox["x"], pox["y"])] = 1
        # Togli la testa
        self.grid[(game_state["you"]["head"]["x"], game_state["you"]["head"]["y"])] = 0
