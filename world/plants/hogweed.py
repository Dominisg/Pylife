from world.plants.plant import Plant
from kivy.core.image import Image
from point import Point

class Hogweed(Plant):

    def __init__(self, cords, world):
        super(Plant, self).__init__(cords, world, 10, 0)
        self._texture = Image("./world/plants/graphics/hogweed.png").texture


    def be_eaten(self,organism):
        self._world.remove_organism(organism)
        self._world.remove_organism(self)

    def action(self):
        tmp = Point(self._cords.x,self._cords.y)
        tmp.x+=1
        self.kill(tmp)
        tmp.x-=2
        self.kill(tmp)
        from world.worldgrid import WorldGrid
        if isinstance(self._world, WorldGrid):
            tmp.x+=1
            tmp.y+=1
            self.kill(tmp)
            tmp.y-=2
            self.kill(tmp)
        else:
            if tmp.y%2==1:
                tmp.x+=1
                tmp.y-=1
            else:
                tmp.y-=1
            self.kill(tmp)
            tmp.x+=1
            tmp.y+=2
            self.kill(tmp)
            tmp.x-=1
            tmp.y+=2
            self.kill(tmp)
        super(Hogweed,self).action()


    def kill(self,tmp):
        organism = self._world.is_there(tmp)
        if organism:
            if not(isinstance(organism,Plant)):
                self._world.remove_organism(organism)
                #comment killing