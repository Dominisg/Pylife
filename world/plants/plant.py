from world.organism import Organism
import random

class Plant(Organism):
    def __init__(self, cord, world, str, ini):
        super(Organism, self).__init__(cord, world, str, ini)

    def will_it_fend(self,attacket):
        return False

    def will_it_escape(self):
        return False

    def be_eaten(self,organism):
        self._world.remove_organism(self)

    def action(self):
        self.spread()

    def spread(self):
        if random.randrange(0, 100) + 1 <= 10:
            if self._world.create_in_neighbourhood(self._cords,type(self).__name__):
                self._world.get_commentator().comment_spreading(self)
                return True
        return False