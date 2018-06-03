from point import Point
from world.animals.sheep import Sheep
from world.animals.turtle import Turtle
from world.animals.fox import Fox
from world.animals.wolf import Wolf
from world.animals.antelope import Antelope
from world.plants.dandelion import Dandelion
from world.plants.deadlyshade import Deadlyshade
from world.plants.grass import Grass
from world.plants.guarana import Guarana
from world.plants.hogweed import Hogweed


import random


class World:
    screensize = Point(600, 800)

    def __init__(self, dim):
        self.__organisms = []
        self.__created_list = []
        self.__destroy_list = []
        self._dimensions = dim
        self.__boardinterface = None
        self.__human = None
        self.__map = [[0 for x in range(dim.x)] for y in range(dim.y)]
        self.create_starting_board()

    def create_in_neighbourhood(self, point, type):
        pass

    def rand_dir(self):
        pass

    def set_dir(self,dir):
        if self.__human:
            self.__human.set_dir(dir)

    def translate_cords(self, dir, cords):
        pass


    def set_human(self,human):
        self._human=human

    def get_dim(self):
        return self._dimensions

    def get_organisms(self):
        return self.__organisms

    def get_recently_created_organism(self):
        return self.__created_list

    def set_boardinterface(self, bi):
        self.__boardinterface = bi

    def get_boardinterface(self):
        return self.__boardinterface

    def create_starting_board(self):
        # self.create_organism(Sheep.__name__)
        # self.create_organism(Sheep.__name__)
        # self.create_organism(Sheep.__name__)
        self.create_organism("Turtle")
        self.create_organism("Turtle")
        self.create_organism("Fox")
        self.create_organism("Wolf")
        self.create_organism("Wolf")
        self.create_organism("Sheep")
        self.create_organism("Sheep")
        self.create_organism("Antelope")
        self.create_organism("Antelope")
        self.create_organism("Fox")
        self.create_organism("Hogweed")
        self.create_organism("Dandelion")
        self.create_organism("Grass")
        self.create_organism("Deadlyshade")
        self.create_organism("Guarana")



    def perform_round(self):
        for organism in self.__organisms:
            if self.check_if_alive(organism):
                organism.action()
        self.destroy_organisms()
        self.add_created_organism()

    def bubble_organism(self):
        size = len(self.__organisms)
        for i in range(0, size):
            if self.__organisms[size - i - 1].get_initiative() > self.__organisms[size - i - 2].get_initiative():
                self.__organisms[size - i - 2], self.__organisms[size - i - 1] = self.__organisms[size - i - 1], \
                                                                                 self.__organisms[size - i - 2]

    def is_there(self, cords):
        if cords.x >= self._dimensions.x or cords.x < 0 or cords.y >= self._dimensions.y or cords.y < 0:
            return None
        return self.__map[cords.x][cords.y]

    def set_on_board(self, organism):
        self.__map[organism.get_cords().x][organism.get_cords().y] = organism

    def add_created_organism(self):
        while len(self.__created_list) > 0:
            self.set_on_board(self.__created_list[0])
            self.__organisms.append(self.__created_list[0])
            self.__created_list.pop(0)
            self.bubble_organism()

    def take_from_board(self, organism):
        cords = organism.get_cords()
        if self.__map[cords.x][cords.y] == organism:
            self.__map[cords.x][cords.y] = None

    def get_organism(self, cords):
        return self.__map[cords.x][cords.y]

    def destroy_organisms(self):
        found = False
        while len(self.__destroy_list) > 0:
            for i in range(0, len(self.__organisms)):
                if self.__organisms[i] == self.__destroy_list[-1]:
                    self.__organisms.pop(i)
                    found = True
                    break
            if not (found):
                for i in range(0, len(self.__created_list)):
                    if self.__created_list[i] == self.__destroy_list[-1]:
                        self.__created_list.pop(i)
                        break
            found = False
            self.__destroy_list.pop(-1)

    def check_if_alive(self, target):
        for organism in self.__destroy_list:
            if target == organism:
                return False
        return True

    def alloc_by_type(self, type, cords):
        return globals()[type](cords, self)

    def create_organism(self, type):
        do = False
        tmp = Point()
        while self.is_there(tmp) or do == False:
            do = True
            tmp.x = random.randrange(self._dimensions.x)
            tmp.y = random.randrange(self._dimensions.y)

        self.create_organism_c(type, tmp)

    def create_organism_c(self, type, cords):
        organism = self.alloc_by_type(type, cords)
        self.__map[cords.x][cords.y] = organism
        self.__organisms.append(organism)
        # if(type == human)
        self.bubble_organism()
        return organism

    def add_to_queue(self, type, point):
        organism = self.alloc_by_type(type, point)
        self.set_on_board(organism)
        self.__created_list.append(organism)

    def remove_organism(self, target):
        tmp = target.get_cords()

        if self.__map[tmp.x][tmp.y] == target:
            self.__map[tmp.x][tmp.y] = None
        for i in range(0, len(self.__organisms)):
            if self.__organisms[i] == target:
                self.__destroy_list.append(target)
                return

        for i in range(0, len(self.__created_list)):
            if self.__created_list[i] == target:
                self.__destroy_list.append(target)
                return
