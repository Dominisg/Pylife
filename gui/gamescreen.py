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
from kivy.uix.widget import Widget
from world.direction import Direction
from kivy.uix.dropdown import DropDown
from gui.commentator import Commentator
from kivy.uix.popup import Popup
import re
import math

Builder.load_file("gui/life.kv")


class NumberInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        return super(NumberInput, self).insert_text(s, from_undo=from_undo)


class ScrollableLabel(ScrollView):
    pass
    # text = StringProperty('')


class CustomDropDown(DropDown):
    pass


class MyPopup(Popup):
    pass

    def create_organism(self):
        pass


class AnimalFactory(Widget):

    def set_cords(self, c):
        self.__cords = c

    def dismiss(self):
        self.__popup.dismiss()

    def set_pop(self, p):
        self.__popup = p

    def create_organism(self, organism):
        app = App.get_running_app()
        app.get_world().create_organism_c(organism, self.__cords)


class MyKeyboardListener(Widget):

    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        app = App.get_running_app()

        if keycode[1] == 'left' or keycode[1] == 'a':
            app.get_world().set_dir(Direction.LEFT)
            app.set_dir('LEFT')
        if keycode[1] == 'up' or keycode[1] == 'w':
            app.get_world().set_dir(Direction.UP)
            app.set_dir('UP')
        if keycode[1] == 'down' or keycode[1] == 'x':
            app.get_world().set_dir(Direction.DOWN)
            app.set_dir('DOWN')
        if keycode[1] == 'right' or keycode[1] == 'd':
            app.get_world().set_dir(Direction.RIGHT)
            app.set_dir('RIGHT')
        if isinstance(app.get_world(), WorldHex):
            if keycode[1] == 'e':
                app.set_dir('HEXRIGHT')
                app.get_world().set_dir(Direction.HEXRIGHT)
            if keycode[1] == 'z':
                app.set_dir('HEXLEFT')
                app.get_world().set_dir(Direction.HEXLEFT)
        return True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            print(touch.pos)
            if touch.pos[1] < 760 and touch.pos[1] > 170:
                if isinstance(app.get_world(), WorldGrid):
                    cords = Point(int(touch.pos[0] / (600 / app.get_world().get_dim().x)),
                                  int((touch.pos[1] - 170) / (600 / app.get_world().get_dim().y)))
                    print(cords.x, cords.y)
                    if app.get_world().is_there(cords) == 0:
                        self.showmenu(cords)
                else:
                    dimensions = app.get_world().get_dim()
                    if dimensions.x > dimensions.y:
                        dim = dimensions.x + 1
                        difference = dim - dimensions.y
                    else:
                        dim = dimensions.y + 1
                        difference = dim - dimensions.x

                    translation = int((600 / dim / math.sqrt(3)) / 2)
                    cords = Point(0,
                                  int((touch.pos[1] - translation - 180) / ((600 / dim / math.sqrt(3)) * (3 / 2))))

                    if cords.y % 2 == 0:
                        cords.x = int(((touch.pos[0] - 10) / (600 / dim)))
                    else:
                        cords.x = int(((touch.pos[0] - 10 - (300 / dim)) / (600 / dim)))
                    cords.y -= difference
                    cords.y = dimensions.y - cords.y - 1
                    print(cords.x, cords.y)

                    if cords.x >= 0 and cords.y >= 0 and cords.x < dimensions.x and cords.y < dimensions.y and app.get_world().is_there(
                            cords) == 0:
                        self.showmenu(cords)

    def showmenu(self, cords):
        animalfactory = AnimalFactory()
        animalfactory.set_cords(cords)
        popup = MyPopup(content=animalfactory)
        animalfactory.set_pop(popup)
        popup.open()


class Dialog(Screen):

    def __init__(self):
        super(Screen, self).__init__()

    def create_world(self, x, y, hexvalue):
        if not x or not y:
            x = 10
            y = 10
        if int(x) < 5:
            x = 5
        if int(y) < 5:
            y = 5

        if hexvalue == 'down':
            self.__world = WorldHex(Point(int(x), int(y)))
        else:
            self.__world = WorldGrid(Point(int(x), int(y)))

    def get_world(self):
        return self.__world


class BoardInterface(Screen):

    def __init__(self):
        super(Screen, self).__init__()

    def on_enter(self, *args):
        Window.size = (600, 800)
        self.__app.init()
        self.__app.print()
        self.add_widget(MyKeyboardListener())

    def set_app(self, app):
        self.__app = app

    def clear(self):
        self.canvas.remove_group("board")
        self.canvas.ask_update()
        self.__app.print()


class LifeApp(App):
    dir = StringProperty("RIGHT")
    info = StringProperty("You can use your skill")
    text = StringProperty('')

    def __init__(self):
        super(LifeApp, self).__init__()
        Window.size = (300, 100)
        self.__dialog = Dialog()
        self.__boardinterface = BoardInterface()
        self.__screen_manager = ScreenManager()
        self.__screen_manager.add_widget(self.__dialog)
        self.__screen_manager.add_widget(self.__boardinterface)
        self.__boardinterface.set_app(self)

    def clear(self):
        self.__boardinterface.clear()

    def set_dir(self, d):
        self.dir = d

    def set_info(self, l):
        self.info = l

    def set_text(self, l):
        self.text += l

    def perform_round(self):
        self.text = ""
        self.__world.perform_round()

    def get_world(self):
        return self.__world

    def init(self):
        self.__world = self.__dialog.get_world()
        self.__world.set_boardinterface(self.__boardinterface)
        self.__commentator = Commentator(self)
        self.__world.set_commentator(self.__commentator)

    def print(self):
        interface_size = Point(600, 600)
        dimensions = self.__world.get_dim()
        if isinstance(self.__world, WorldHex):
            with self.__boardinterface.canvas:
                Color(1, 1, 1, 1)
                if dimensions.x > dimensions.y:
                    dim = dimensions.x + 1
                else:
                    dim = dimensions.y + 1
                for j in range(1, dimensions.y + 1):
                    for i in range(1, dimensions.x * 2 + 1, 2):
                        if j % 2 == 1:
                            Line(points=self.get_hex_corners(Point(10 + (i * (600 / dim) / 2), 750 - (
                                    600 / dim + (j - 1) * 3 * (600 / dim) / 2 / math.sqrt(3))),
                                                             600 / dim / math.sqrt(3)), group="board")
                        else:
                            Line(points=self.get_hex_corners(Point(10 + 300 / dim + (i * (600 / dim) / 2), 750 - (
                                    600 / dim + (j - 1) * 3 * (600 / dim) / 2 / math.sqrt(3))),
                                                             600 / dim / math.sqrt(3)), group="board")

        else:
            with self.__boardinterface.canvas:
                Color(1, 1, 1, 0.4)
                for i in range(0, dimensions.x, 2):
                    Rectangle(pos=(i * (interface_size.x / dimensions.x), 170),
                              size=(interface_size.x / dimensions.x, interface_size.y), group="board")
                for i in range(0, dimensions.y, 2):
                    Rectangle(pos=(0, i * (interface_size.y / dimensions.y) + 170),
                              size=(interface_size.x, interface_size.y / dimensions.y), group="board")
        organisms = self.__world.get_organisms()
        self.__boardinterface.canvas.add(Color(1, 1, 1, 1))
        for organism in organisms:
            organism.draw()

    def build(self):
        return self.__screen_manager

    def get_hex_corners(self, cords, size):
        point = []
        for i in range(0, 7):
            point.append(Point())
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            point[i].x = cords.x + size * math.cos(angle_rad)
            point[i].y = cords.y + size * math.sin(angle_rad)

        return (
            point[0].x, point[0].y, point[1].x, point[1].y, point[2].x, point[2].y, point[3].x, point[3].y, point[4].x,
            point[4].y, point[5].x, point[5].y, point[6].x, point[6].y, point[0].x, point[0].y)
