from point import Point
from world.animals.sheep import Sheep
from world.animals.turtle import Turtle
from world.animals.fox import Fox
from world.animals.wolf import Wolf
from world.animals.antelope import Antelope
from world.animals.human import Human
from world.plants.dandelion import Dandelion
from world.plants.deadlyshade import Deadlyshade
from world.plants.grass import Grass
from world.plants.guarana import Guarana
from world.plants.hogweed import Hogweed
from world.animals.cybersheep import Cybersheep
from abc import ABC, abstractmethod

import random


class World(ABC):
    screensize = Point(600, 800)

    def __init__(self, dim):
        self.__organisms = []
        self.__created_list = []
        self.__destroy_list = []
        self.__commentator = 0
        self._dimensions = dim
        self.__boardinterface = None
        self.__human = None
        self.__map = [[0 for y in range(dim.y)] for x in range(dim.x)]
        self.create_starting_board()

    @abstractmethod
    def create_in_neighbourhood(self, point, type):
        pass

    @abstractmethod
    def rand_dir(self):
        pass

    def set_dir(self, dir):
        if self.__human:
            self.__human.set_dir(dir)

    def set_commentator(self, com):
        self.__commentator = com

    def get_commentator(self):
        return self.__commentator

    def translate_cords(self, dir, cords):
        pass

    def activate_skill(self):
        if self.__human:
            self.__human.activate_skill()

    def set_human(self, human):
        self.__human = human

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
        pass
        self.create_organism("Turtle")
        self.create_organism("Turtle")
        self.create_organism("Human")
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
        self.create_organism("Cybersheep")

    def perform_round(self):
        for organism in self.__organisms:
            if self.check_if_alive(organism):
                organism.action()
        self.destroy_organisms()
        self.add_created_organism()

    def bubble_organism(self):
        size = len(self.__organisms)
        for i in range(0, size - 1):
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
            self.__map[cords.x][cords.y] = 0

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
            if not found:
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
        self.bubble_organism()
        return organism

    def add_to_queue(self, type, point):
        organism = self.alloc_by_type(type, point)
        self.set_on_board(organism)
        self.__created_list.append(organism)

    def remove_organism(self, target):
        tmp = target.get_cords()

        if self.__map[tmp.x][tmp.y] == target:
            self.__map[tmp.x][tmp.y] = 0
        for i in range(0, len(self.__organisms)):
            if self.__organisms[i] == target:
                self.__destroy_list.append(target)
                return

        for i in range(0, len(self.__created_list)):
            if self.__created_list[i] == target:
                self.__destroy_list.append(target)
                return

    def save(self):
        try:
            file = open("save.txt", "wt")

            file.write(str(self._dimensions.x) + " " + str(self._dimensions.y) + "\n")
            for organism in self.__organisms:
                organism.save_me(file)

            file.close()
        except IOError:
            print("Error: File does not appear to exist.")

    def load(self):
        try:
            file = open("save.txt", "r")
            self.__map = None
            self.__organisms.clear()
            self.__created_list.clear()
            self.__destroy_list.clear()

            a = [int(x) for x in file.readline().split()]
            self._dimensions.x = a[0]
            self._dimensions.y = a[1]
            self.__map = [[0 for y in range(self._dimensions.y)] for x in range(self._dimensions.x)]
            while True:
                a.clear()
                a = [x for x in file.readline().split()]
                if len(a) < 2: break
                cords = Point(int(a[1]), int(a[2]))
                organism = self.create_organism_c(a[0], cords)
                organism.set_strenght(int(a[3]))
                if type(organism) == Human:
                    organism.set_cooldown(int(a[4]))
            file.close()
        except IOError:
            print("Error: File does not appear to exist.")
