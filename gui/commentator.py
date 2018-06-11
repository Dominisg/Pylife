class Commentator:

    def __init__(self, app):
        self.__app = app

    def comment_fight(self, attacker, target):
        self.__app.set_text(type(attacker).__name__ + " attacked " + type(target).__name__ + "\n")

    def comment_fight_result(self, attacker, win):
        if win:
            self.__app.set_text(type(attacker).__name__ + " won " + "\n")
        else:
            self.__app.set_text(type(attacker).__name__ + " lost " + "\n")

    def comment_jumping(self, organism, point):
        self.__app.set_text(type(organism).__name__ + " jumped on filed (" + str(point.x) +","+ str(point.y) + ")\n")

    def comment_movement(self, organism, dir):
        cords = organism.get_cords()
        self.__app.set_text(type(organism).__name__ + "(" + str(cords.x) + "," + str(cords.y) + ') moved ' + dir.name + '\n')

    def comment_porliferation(self, organism, success):
        cords = organism.get_cords()
        if success:
            self.__app.set_text(
                type(organism).__name__ + "(" + str(cords.x) + "," + str(cords.y) + ') reproduced themselves with success\n')
        else:
            self.__app.set_text(
                type(organism).__name__ + "(" + str(cords.x) + "," + str(cords.y) + ') tried to reproduce themselves\n')

    def comment_eating(self, plant, animal):
        cords = plant.get_cords()
        self.__app.set_text(
            type(plant).__name__ + "(" + str(cords.x) + "," + str(cords.y) + ') was eaten by ' + type(animal).__name__ + '\n')

    def comment_killing(self, plant, animal):
        cords = plant.get_cords()
        self.__app.set_text(
            type(plant).__name__ + "(" + str(cords.x) + "," + str(cords.y) + ') killed ' + type(animal).__name__ + '\n')

    def comment_spreading(self, plant):
        cords = plant.get_cords()
        self.__app.set_text(type(plant).__name__ + "(" + str(cords.x) + "," + str(cords.y) + ') spread\n')

