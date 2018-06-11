from world.animals.sheep import Animal
from kivy.core.image import Image
from world.plants.hogweed import Hogweed
from point import Point

class Cybersheep(Animal):
    def __init__(self,cords,world):
        super(Animal,self).__init__(cords, world,11,4)
        self.__supertexture=Image("./world/animals/graphics/cybersheep.png").texture
        self.__texture=Image("./world/animals/graphics/sheep.png").texture
        self._texture = self.__texture
        for organism in self._world.get_organisms():
            if(isinstance(organism,Hogweed)):
                self._texture = self.__supertexture



    def track_nearest_enemy(self):
        way = 0
        nearest = None
        for organism in self._world.get_organisms():
            if(isinstance(organism,Hogweed)):
                enemycords = organism.get_cords()
                currentway = abs(enemycords.x-self._cords.x) + abs(enemycords.y-self._cords.x)
                if way==0 or way > currentway:
                    way = currentway
                    nearest = organism

        return nearest



    def action(self):
        enemy = self.track_nearest_enemy()
        if enemy == None:
            self._texture = self.__texture
            super(Cybersheep,self).action()
            return
        else:
            self._texture = self.__supertexture
            self._world.take_from_board(self)
            last_cords = Point(self._cords.x, self._cords.y)
            dir = self._world.best_way_to(self._cords,enemy.get_cords())
            self._world.get_commentator().comment_movement(self, dir)
            collision_target = self.move(dir)
            if collision_target:
                self.collision(collision_target, last_cords)
            if self._world.check_if_alive(self):
                self._world.set_on_board(self)




