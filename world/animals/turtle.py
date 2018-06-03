from world.animals.animal import Animal
from kivy.core.image import Image
import random


class Turtle(Animal):
    def __init__(self, cords, world):
        super(Animal, self).__init__(cords, world, 2, 1)
        self._texture = Image("./world/animals/graphics/turtle.png").texture

    def action(self):
        if random.randrange(0,4) == 0:
            super(Turtle, self).action()

    def will_it_fend(self, attacker):
        return attacker.get_strenght() < 5
