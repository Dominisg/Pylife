from world.animals.animal import Animal
from kivy.core.image import Image
from point import Point
from world.direction import Direction
import random


class Antelope(Animal):
    def __init__(self,cords,world):
        super(Animal, self).__init__(cords, world, 4, 4)
        self._texture = Image("./world/animals/graphics/antelope.png").texture

    def action(self):
        self._world.take_from_board(self)
        last_cords = Point(self._cords.x,self._cords.y)

        while True:
            dir = self._world.rand_dir()
            if self.will_be_in(dir):
                break

        self.move(dir)

        while True:
            dir = self._world.rand_dir()
            if self.will_be_in(dir):
                break

        collision_target = self.move(dir)

        if self._cords.x == last_cords.x and self._cords.y == last_cords.y:
            self._world.set_on_board(self)
            self.action()
        else:
            #todo: comment
            if collision_target:
                self.collision(collision_target,last_cords)
            if self._world.check_if_alive(self):
                self._world.set_on_board(self)

    def will_it_escape(self):
        tmp = Point(self._cords.x,self._cords.y)
        self._world.take_from_board(self)
        if random.randrange(0,2):
                if self.will_be_in(Direction.RIGHT):
                    if not(self.move(Direction.RIGHT)):
                        self._world.set_on_board(self)
                        return True
                    else:
                        self.go_back(tmp)

                if self.will_be_in(Direction.LEFT):
                    if not (self.move(Direction.LEFT)):
                        self._world.set_on_board(self)
                        return True
                    else:
                        self.go_back(tmp)

                if self.will_be_in(Direction.UP):
                    if not(self.move(Direction.UP)):
                        self._world.set_on_board(self)
                        return True
                    else:
                        self.go_back(tmp)

                if self.will_be_in(Direction.DOWN):
                    if not(self.move(Direction.DOWN)):
                        self._world.set_on_board(self)
                        return True
                    else:
                        self.go_back(tmp)

                from world.worldhex import WorldHex
                if isinstance(self._world, WorldHex):
                    if self.will_be_in(Direction.HEXLEFT):
                        if not (self.move(Direction.HEXLEFT)):
                            self._world.set_on_board(self)
                            return True
                        else:
                            self.go_back(tmp)

                    if self.will_be_in(Direction.HEXRIGHT):
                        if not (self.move(Direction.HEXRIGHT)):
                            self._world.set_on_board(self)
                            return True
                        else:
                            self.go_back(tmp)




