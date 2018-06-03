from world.animals.animal import Animal
from world.direction import Direction
from kivy.core.image import Image

class Human(Animal):
    def __init__(self,cords,world):
        super(Animal,self).__init__(cords, world,4,4)
        self._texture = Image("./world/animals/graphics/human.png").texture
        self.__skill_is_active = False
        self.__dir = Direction.RIGHT

    def set_cooldown(self,cld):
        self.__cooldown=cld
        if cld>0:
            self.__skill_is_active = True

    def get_coodown(self):
        return self.__cooldown





