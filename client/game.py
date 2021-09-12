from ursina import *
from snake import *

app = Ursina()

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

app.run()