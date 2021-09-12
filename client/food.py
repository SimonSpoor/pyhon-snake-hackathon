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
        coords = (random.random() * 18 - 9, random.random() * 18 - 9)
        self.position = (coords[0], self.model_bounds.y / 2, coords[1])
        print(coords)