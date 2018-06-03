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
            app.get_world.set_dir(Direction.LEFT)
            app.set_dir('LEFT')
        if keycode[1] == 'up' or keycode[1] == 'w':
            app.get_world.set_dir(Direction.UP)
            app.set_dir('UP')
        if keycode[1] == 'down' or keycode[1] == 'x':
            app.get_world.set_dir(Direction.DOWN)
            app.set_dir('DOWN')
        if keycode[1] == 'right' or keycode[1] == 'd':
            app.get_world.set_dir(Direction.RIGHT)
            app.set_dir('RIGHT')
        if keycode[1] == 'e':
            app.set_dir('HEXRIGHT')
            app.get_world.set_dir(Direction.HEXRIGHT)
        if keycode[1] == 'z':
            app.set_dir('HEXLEFT')
            app.get_world.set_dir(Direction.HEXLEFT)

    def on_touch_down(self, touch):
        print (touch.pos)
        



        return True

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

    def __init__(self):
        super(Screen,self).__init__()
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

    def __init__(self):
        super(LifeApp, self).__init__()
        Window.size = (300, 100)
        self.__dialog = Dialog()
        self.__boardinterface = BoardInterface()
        self.__screen_manager = ScreenManager()
        self.__screen_manager.add_widget(self.__dialog)
        self.__screen_manager.add_widget(self.__boardinterface)
        self.__boardinterface.set_app(self)

    def set_dir(self, d):
        self.dir=d

    def perform_round(self):
        self.__world.perform_round()

    def get_world(self):
        return self.__world

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






