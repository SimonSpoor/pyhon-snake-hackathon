from ursina import *
from player import *

app = Ursina()

ground_size = 25
ground=Entity(
    model='quad',
    color=color.gray,
    scale=(ground_size,ground_size),
    position=(0, 0, 0),
    rotation=(90, 0, 0)
)

camera.position = (0, 60, 28)
camera.rotation_x = 65
camera.rotation_y = 180

player = Player()

app.run()