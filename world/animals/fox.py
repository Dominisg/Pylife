from world.animals.animal import Animal
from kivy.core.image import Image
from point import Point
from world.direction import Direction
import random


class Fox(Animal):
    def __init__(self,cords,world):
        super(Animal,self).__init__(cords, world,3,7)
        self._texture = Image("./world/animals/graphics/fox.png").texture

    def action(self):
        self._world.take_from_board(self)
        last_cords = Point(self._cords.x,self._cords.y)
        dir = self.where_fox_goes()
        if dir==None:
            self._world.set_on_board(self)
            return
        #todo:Comment
        collision_target = self.move(dir)
        if collision_target:
            self.collision(collision_target,last_cords)
        if self._world.check_if_alive(self):
            self._world.set_on_board(self)

    def where_fox_goes(self):
        from world.worldhex import WorldHex
        sowhere = []
        sowhere.append(self.can_go_dir(Direction.RIGHT))
        sowhere.append(self.can_go_dir(Direction.LEFT))
        sowhere.append(self.can_go_dir(Direction.DOWN))
        sowhere.append(self.can_go_dir(Direction.UP))


        if isinstance(self._world,WorldHex):
            sowhere.append(self.can_go_dir(Direction.HEXRIGHT))
            sowhere.append(self.can_go_dir(Direction.HEXLEFT))

        suma = 0
        for where in sowhere:
            if where:
                suma += 1

        if suma == 0:
            return None

        while True:
            if isinstance(self._world, WorldHex):
                suma = random.randrange(0,6)
            else:
                suma = random.randrange(0,4)
            if sowhere[suma]:
                return Direction.get_dir(suma)

    def can_go_dir(self,dir):
        if not(self.will_be_in(dir)):
            return False
        tmp = Point(self._cords.x,self._cords.y)
        self._world.translate_cords(dir, tmp)
        if not(self._world.is_there(tmp)) or self._world.is_there(tmp).get_strenght() <= self._strenght:
            return True
        return False
