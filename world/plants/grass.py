from world.plants.plant import Plant
from kivy.core.image import Image

class Grass(Plant):

    def __init__(self, cords, world):
        super(Plant, self).__init__(cords, world, 0, 0)
        self._texture = Image("./world/animals/graphics/grass.png").texture


