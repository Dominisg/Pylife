from world.plants.plant import Plant
from kivy.core.image import Image


class Dandelion(Plant):

    def __init__(self, cords, world):
        super(Plant, self).__init__(cords, world, 0, 0)
        self._texture = Image("./world/plants/graphics/dandelion.png").texture

    def action(self):
        for i in range(0,3):
            if self.spread():
                return

