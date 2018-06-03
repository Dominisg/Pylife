from kivy.graphics import *


class Organism:
    def __init__(self, cords, world, str, ini):
        self._strenght = str
        self._world = world
        self._initiative = ini
        self._cords = cords
        self._texture = None

    def action(self):
        pass

    def will_it_fend(self,attacket):
        pass

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
        dim = self._world.get_dim()
        from world.worldgrid import WorldGrid
        if isinstance(self._world, WorldGrid):
            pos = (self._cords.x * (600 / dim.x), self._cords.y * (600 / dim.y) + 170)
            self._world.get_boardinterface().canvas.add(Rectangle(texture=self._texture, pos=pos, size=(600/dim.x, 600/dim.y), group="board"))
        else:
            pass


