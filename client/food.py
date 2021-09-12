from ursina import *

class Apple(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'assets/apple.obj'
        self.texture = 'assets/apple.png'
        self.collider ='sphere'
        self.color = color.red
        self.relocate_apple()

    def relocate_apple(self):
        coords = (random.random() * 44 - 22, random.random() * 20 - 10)
        self.position = (coords[0], self.model_bounds.y / 2, coords[1])
        print(coords)