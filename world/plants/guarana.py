from world.plants.plant import Plant
from kivy.core.image import Image

class Guarana(Plant):

    def __init__(self, cords, world):
        super(Plant, self).__init__(cords, world, 0, 0)
        self._texture = Image("./world/plants/graphics/guarana.png").texture

    def be_eaten(self,organism):
        organism.set_strenght(organism.get_strenght()+3)
        self._world.remove_organism(self)


