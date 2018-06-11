from kivy.graphics import *
import math
from abc import ABC, abstractmethod


class Organism(ABC):
    def __init__(self, cords, world, str, ini):
        self._strenght = str
        self._world = world
        self._initiative = ini
        self._cords = cords
        self._texture = None

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def will_it_fend(self,attacket):
        pass

    @abstractmethod
    def will_it_escape(self):
        pass


    def get_strenght(self):
        return self._strenght


    def set_strenght(self, str):
        return self._strenght


    def get_initiative(self):
        return self._initiative

    def get_cords(self):
        return self._cords

    def draw(self):
        dime = self._world.get_dim()
        from world.worldgrid import WorldGrid
        if isinstance(self._world, WorldGrid):
            pos = (self._cords.x * (600 / dime.x), self._cords.y * (600 / dime.y) + 170)
            self._world.get_boardinterface().canvas.add(Rectangle(texture=self._texture, pos=pos, size=(600/dime.x, 600/dime.y), group="board"))
        else:
            if dime.x > dime.y:
                dim=dime.x+1
            else:
                dim =dime.y+1

            if self._cords.y % 2 == 0:
                pos = (10 + (self._cords.x*2) *(600/dim)/2) ,750 - (600/dim/2 + (600/dim + (self._cords.y)*3*(600/dim)/2/math.sqrt(3)))
            else:
                pos = (10 + 300/dim+((self._cords.x*2) *(600/dim)/2),750 - (600/dim/2 +  (600/dim + (self._cords.y)*3*(600/dim)/2/math.sqrt(3))))


            self._world.get_boardinterface().canvas.add(Rectangle(texture=self._texture, pos=pos, size=(600/dim, 600/dim), group="board"))

    def save_me(self,file):
        file.write(type(self).__name__+" ")
        file.write(str(self._cords.x) + " " +str(self._cords.y) + " " +str(self._strenght)+'\n')




