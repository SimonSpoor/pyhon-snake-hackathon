from ursina import *
from snake import *

class Menu():
    def __init__(self):
        self.singleplayerButton = Button('Singleplayer', text_origin=(0, 0.15), on_click=self.loadSingleplayerGame)
        self.multiplayerButton = Button('Multiplayer', text_origin=(0, -0.15), on_click=self.loadMultiplayerGame)

    def showMenu(self):
        self.singleplayerButton.enabled = True
        self.multiplayerButton.enabled = True

    def hideMenu(self):
        self.singleplayerButton.enabled = False
        self.multiplayerButton.enabled = False

    def loadMultiplayerGame(self):
        hostTitle = Text(text='Enter Server IP:', origin=(0, 0.15))
        hostInput = InputField(default_value='127.0.0.1', label='Host Address', origin=(0, -0.15))
        self.hideMenu()

    def loadSingleplayerGame(self):
        ground_size = 3
        ground=Entity(
            model='assets/grass.obj',
            texture="assets/grass.jpg",
            scale=(ground_size,ground_size),
            position=(0, 0, 0),
            rotation=(0, 0, 0)
        )

        camera.position = (0, 60, 28)
        camera.rotation_x = 65
        camera.rotation_y = 180

        player = Snake()
        self.hideMenu()