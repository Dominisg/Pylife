from world.animals.animal import Animal
from world.direction import Direction
from kivy.core.image import Image
from kivy.app import App
from point import Point
import random

class Human(Animal):
    def __init__(self,cords,world):
        super(Animal,self).__init__(cords, world,5,4)
        self._texture = Image("./world/animals/graphics/human.png").texture
        self.__skill_is_active = False
        self.__dir = Direction.RIGHT
        self.__app = App.get_running_app()
        self.__cooldown = -5
        world.set_human(self)

    def set_cooldown(self,cld):
        self.__cooldown=cld
        if cld>0:
            self.__skill_is_active = True

    def get_coodown(self):
        return self.__cooldown

    def set_dir(self,d):
        self.__dir =d


    def action(self):
        if not self.__skill_is_active and self.__cooldown >= -5:
            self.__app.set_info("You can't use skill")
        last_cords = Point(self._cords.x,self._cords.x)
        self._world.take_from_board(self)
        if self.will_be_in(self.__dir):
            collision_target = self.move(self.__dir)

            if self.__skill_is_active and self.will_be_in(self.__dir):
                if(self.__cooldown>=2 or random.randrange(0,2)):
                    collision_target = self.move(self.__dir)
            if collision_target:
                self.collision(collision_target,last_cords)
        if self._world.check_if_alive(self):
            self._world.set_on_board(self)
        self.__cooldown-=1
        if self.__cooldown <=0:
            self.__skill_is_active = False
            self.__app.set_info("You can't use your skill")
        if self.__cooldown <=-5:
            self.__app.set_info("You can use your skill")


    def activate_skill(self):
        self.__app.set_info("Skill is active")
        if self.__cooldown <= -5:
            self.__skill_is_active = True
            self.__cooldown = 5

    def save_me(self,file):
        file.write(type(self).__name__+" ")
        file.write(str(self._cords.x) + " " +str(self._cords.y) + " " +str(self._strenght) +" "+str(self.__cooldown)+"\n")


