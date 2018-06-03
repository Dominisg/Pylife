from world.world import World
from world.direction import Direction
from point import Point


class WorldGrid(World):
    def __init__(self, dim):
        super(WorldGrid, self).__init__(dim)

    def rand_dir(self):
        return Direction.random_direction()

    def translate_cords(self, dire, cords):
        dire.translate(cords)

    def create_in_neighbourhood(self, point, type):
        tmp = Point(point.x, point.y)
        tmp.x += 1
        if tmp.x < self._dimensions.x and not (self.is_there(tmp)):
            self.add_to_queue(type, tmp)
            return True
        tmp.x -= 2
        if tmp.x >= 0 and not (self.is_there(tmp)):
            self.add_to_queue(type, tmp)
            return True
        tmp.x += 1
        tmp.y += 1
        if tmp.y < self._dimensions.y and not(self.is_there(tmp)):
            self.add_to_queue(type, tmp)
            return True
        tmp.y -= 2
        if  tmp.y >= 0 and not (self.is_there(tmp)):
            self.add_to_queue(type, tmp)
            return True

        return False
