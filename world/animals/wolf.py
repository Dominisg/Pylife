from world.animals.animal import Animal
from kivy.core.image import Image


class Wolf(Animal):
    def __init__(self,cords,world):
        super(Animal,self).__init__(cords, world, 9, 5)
        self._texture = Image("./world/animals/graphics/wolf.png").texture


