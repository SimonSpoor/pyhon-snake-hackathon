from ursina import *
from snake import *

class Menu():
    def __init__(self):
        self.singleplayerButton = Button('Singleplayer', position=(0, 0.15), on_click=self.loadSingleplayerGame)
        self.multiplayerButton = Button('Multiplayer', position=(0, -0.15), on_click=self.loadMultiplayerGame)
        self.singleplayerButton.fit_to_text(radius=0.01)
        self.multiplayerButton.fit_to_text(radius=0.01)

    def showMenu(self):
        self.singleplayerButton.enabled = True
        self.multiplayerButton.enabled = True

    def hideMenu(self):
        self.singleplayerButton.enabled = False
        self.multiplayerButton.enabled = False

    def loadMultiplayerGame(self):
        hostTitle = Text(text='Enter Server IP:', origin=(0, 0))
        hostInput = InputField(origin=(0, 0))
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

        camera.position = (0, 60, 0)
        camera.rotation_x = 90
        camera.rotation_y = 180

        player = Snake()
        self.hideMenu()
