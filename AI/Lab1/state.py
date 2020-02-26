class State:
    # array with the position of the people in the order w1, w2,... h1, h2, ... (0 for initial shore, 1 for goal shore)
    shore = None
    boat = 0
    depth = 0
    # array of States that lead to the current State
    path = None

    def __init__(self, shore=None, boat=0):
        if shore is None:
            shore = []
        self.shore = shore
        self.boat = boat
        self.depth = 0
        self.path = []
