from world.animals.animal import Animal
from kivy.core.image import Image

class Sheep(Animal):
    def __init__(self,cords,world):
        super(Animal,self).__init__(cords, world,4,4)
        self._texture = Image("./world/animals/graphics/sheep.png").texture


