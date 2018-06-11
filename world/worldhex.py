from world.world import World
from world.direction import Direction
from point import Point


class WorldHex(World):
    def __init__(self, dim):
        super(WorldHex, self).__init__(dim)

    def rand_dir(self):
        return Direction.random_direction_hex()

    def translate_cords(self, dire, cords):
        dire.translate_hex(cords)

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
        if tmp.y%2 == 0:
            tmp.x+=1
        tmp.y -= 1
        if tmp.x < self._dimensions.x and tmp.x>=0 and tmp.y>=0 and not (self.is_there(tmp)):
            self.add_to_queue(type, tmp)
            return True

        tmp.y += 2
        tmp.x += 1
        if tmp.x < self._dimensions.x and tmp.y < self._dimensions.y and not (self.is_there(tmp)):
            self.add_to_queue(type, tmp)
            return True

        tmp.y-=2
        if tmp.x < self._dimensions.x  and tmp.y>=0 and not (self.is_there(tmp)):
            self.add_to_queue(type, tmp)
            return True

        tmp.y += 2
        tmp.x +=1
        if tmp.x < self._dimensions.x and tmp.y < self._dimensions.y and not (self.is_there(tmp)):
            self.add_to_queue(type, tmp)
            return True

    def best_way_to(self,start,end):
        if(start.y%2==1):
            if start.x != end.x and start.y != end.y :#change two coordinates
                if start.x < end.x and start.y < end.y:
                    return Direction.DOWN
                if start.x < end.x and start.y > end.y:
                    return Direction.HEXRIGHT

            if start.y != end.y:
                if start.y > end.y:
                    return Direction.UP
                else:
                    return Direction.HEXLEFT

            if start.x != end.x:
                if start.x > end.x:
                    return Direction.LEFT
                else:
                    return Direction.RIGHT



        else:
            if start.x != end.x and start.y != end.y:  # change two coordinates
                if start.x > end.x and start.y > end.y:
                    return Direction.UP
                if start.x > end.x and start.y < end.y:
                    return Direction.HEXLEFT

            if start.y != end.y:
                if start.y > end.y:
                    return Direction.HEXRIGHT
                else:
                    return Direction.DOWN

            if start.x != end.x:
                if start.x > end.x:
                    return Direction.LEFT
                else:
                    return Direction.RIGHT

