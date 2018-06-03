from world.plants.plant import Plant
from kivy.core.image import Image


class Deadlyshade(Plant):

    def __init__(self, cords, world):
        super(Plant, self).__init__(cords, world, 99, 0)
        self._texture = Image("./world/plants/graphics/deadlyshade.png").texture

    def be_eaten(self,organism):
        self._world.remove_organism(organism)
        self._world.remove_organism(self)

