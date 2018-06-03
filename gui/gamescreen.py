from kivy.graphics import *
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App
from world.worldgrid import WorldGrid
from world.worldhex import WorldHex
from point import Point
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
import re

Builder.load_file("gui/life.kv")


class NumberInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        return super(NumberInput, self).insert_text(s, from_undo=from_undo)


class GridBoard(Canvas):
    def __init__(self):
        super(Canvas, self).__init__()
        Rectangle(pos=(10, 10), size=(20, 20))

class ScrollableLabel(ScrollView):
    text = StringProperty('')



class HexBoard(Canvas):
    def __init__(self):
        super(Canvas, self).__init__()
        pass


class Dialog(Screen):


    def __init__(self):
        super(Screen, self).__init__()

    def create_world(self, x, y, hexvalue):
        if hexvalue == 'down':
            self.__world = WorldHex(Point(int(x), int(y)))
        else:
            self.__world = WorldGrid(Point(int(x), int(y)))


    def get_world(self):
        return self.__world


class BoardInterface(Screen):
    def on_enter(self, *args):
        Window.size = (600, 800)
        self.__app.init()
        self.__app.print()


    def perform_round(self):
        self.__app.perform_round()


    def set_app(self, app):
        self.__app = app

    def clear(self):
        self.canvas.remove_group("board")
        self.canvas.ask_update()
        self.__app.print()





class LifeApp(App):

    def __init__(self):
        super(LifeApp, self).__init__()
        Window.size = (300, 100)
        self.__dialog = Dialog()
        self.__boardinterface = BoardInterface()
        self.__screen_manager = ScreenManager()
        self.__screen_manager.add_widget(self.__dialog)
        self.__screen_manager.add_widget(self.__boardinterface)
        self.__boardinterface.set_app(self)

    def perform_round(self):
        self.__world.perform_round()

    def init(self):
        self.__world = self.__dialog.get_world()
        self.__world.set_boardinterface(self.__boardinterface)


    def print(self):
        interface_size = Point(600, 600)
        dimensions = self.__world.get_dim()
        if isinstance(self.__world, WorldHex):
            with self.__boardinterface.canvas:
                Color(0, 0, 1, 0.2)

        else:
            with self.__boardinterface.canvas:
                Color(1, 1, 1, 0.4)
                for i in range(0, dimensions.x, 2):
                    Rectangle(pos=(i*(interface_size.x/dimensions.x), 170), size=(interface_size.x/dimensions.x, interface_size.y), group="board")
                    Rectangle(pos=(0, i*(interface_size.y/dimensions.y)+170), size=(interface_size.x, interface_size.y/dimensions.y), group="board")

        organisms = self.__world.get_organisms()
        self.__boardinterface.canvas.add(Color(1, 1, 1, 1))
        for organism in organisms:
            organism.draw()

    def build(self):
        return self.__screen_manager






