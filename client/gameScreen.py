import ursina
from ursina import *
from snake import *


def loadSGame():
    ground_size = 25    
    ground = Entity(
    model='quad',
    color=color.gray,
    scale=(ground_size,ground_size),
    position=(0, 0, 0),
    rotation=(90, 0, 0))

    camera.position = (0, 60, 28)
    camera.rotation_x = 65
    camera.rotation_y = 180

    player = Snake()

    unloadMenu()

def loadMGame():
    hostTitle = Text(text='Enter Server IP:', origin=(0, 0.15))
    hostInput = InputField(default_value='127.0.0.1', label='Host Address', origin=(0, -0.15))
    unloadMenu()

def showMenu():
    global playS
    global playM
    playS = Button('Singleplayer', text_origin=(0, 0.15), on_click=loadSGame)
    playM = Button('Multiplayer', text_origin=(0, -0.15), on_click=loadMGame)

def unloadMenu():
    playS.enabled = False
    playM.enabled = False

if __name__ == '__main__':
    app = Ursina()
    showMenu()
    app.run()