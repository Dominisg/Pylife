from world.world import World
from world.direction import Direction

class WorldHex(World):
    def __init__(self, dim):
        super(WorldHex, self).__init__(dim)

    def rand_dir(self):
        return Direction.random_direction_hex()

    def translate_cords(self, dire, cords):
        dire.translate(cords)
