from world.organism import Organism
from point import Point


class Animal(Organism):
    def __init__(self, cord, world, str, ini):
        super(Organism, self).__init__(cord, world, str, ini)

    def will_it_fend(self, attacket):
        return False

    def will_it_escape(self):
        return False

    def action(self):
        self._world.take_from_board(self)
        last_cords = Point(self._cords.x, self._cords.y)

        while True:
            dir = self._world.rand_dir()
            if self.will_be_in(dir):
                break
        self._world.get_commentator().comment_movement(self,dir)
        collision_target = self.move(dir)
        if collision_target:
            self.collision(collision_target, last_cords)
        if self._world.check_if_alive(self):
            self._world.set_on_board(self)

    def move(self, dir):
        tmp = Point(self._cords.x, self._cords.y)
        self._world.translate_cords(dir, tmp)
        result = self._world.is_there(tmp)
        self._world.translate_cords(dir, self._cords)
        return result

    def will_be_in(self, dir):
        dim = self._world.get_dim()
        tmp = Point(self._cords.x, self._cords.y)
        self._world.translate_cords(dir, tmp)
        return tmp.x < dim.x and tmp.y < dim.y and tmp.x >= 0 and tmp.y >= 0

    def collision(self, collision_target, last_cords):

        if isinstance(collision_target, Animal):
            if type(collision_target) == type(self):
                self.go_back(last_cords)
                self._world.set_on_board(self)
                self.porliferation(collision_target)
                self._world.take_from_board(self)
            else:
                if collision_target.will_it_fend(self):
                    self.go_back(last_cords)
                else:
                    self.fight(collision_target)
        else:
            self._world.get_commentator().comment_eating(collision_target,self)
            collision_target.be_eaten(self)

    def go_back(self, last_cords):
        self._cords.x = last_cords.x
        self._cords.y = last_cords.y

    def fight(self, collision_target):
        if collision_target.will_it_escape():return
        self._world.get_commentator().comment_fight(self,collision_target)
        if self._strenght >= collision_target.get_strenght():
            self._world.remove_organism(collision_target)
            self._world.get_commentator().comment_fight_result(self, True)
        else:
            self._world.remove_organism(self)
            if self._world.check_if_alive(collision_target):
                self._world.set_on_board(collision_target)
            self._world.get_commentator().comment_fight_result(self, False)

    def porliferation(self, partner):
        if self._world.create_in_neighbourhood(partner.get_cords(), type(self).__name__):
            self._world.get_commentator().comment_porliferation(self, True)
            return
        if self._world.create_in_neighbourhood(self._cords, type(self).__name__):
            self._world.get_commentator().comment_porliferation(self, True)
            return

        self._world.get_commentator().comment_porliferation(self, False)

