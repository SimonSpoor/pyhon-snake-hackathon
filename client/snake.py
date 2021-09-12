from ursina import *
from food import Apple
import time

textures = [
    'default',
    'blue',
    'cyan',
    'darkgreen',
    'green',
    'magenta',
    'orange',
    'pink',
    'purple',
    'red',
    'white',
    'yellow'
]

food = Apple()

class Action():
    def __init__(self, direction, position):
        self.direction = direction
        self.position = position
        self.time = time.time()
        self.completed_indices = []

class GenericSnakeComponent(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._direction = (0, 0)
        self.texture_color = textures[0]

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value
        self.rotate_component()

    def rotate_component(self):
        rotation = self.rotation
        rotation.y = math.atan2(self.direction[0], self.direction[1]) * 180 / math.pi + 180
        self.rotation = rotation

class Snake(GenericSnakeComponent):
    def __init__(self, parent):
        super().__init__()
        self.skin='default'
        self.model='assets/snakes/head.obj'
        self.set_texture()
        self.collider = 'box'
        self.direction = (0, 0)
        self.position = (0, self.model_bounds.y / 2, 0)
        self.children = []
        self.actions = []
        self.__parent = parent

    def set_texture(self):
        self.texture = 'assets/snakes/{0}/head.png'.format(self.skin)

    @property
    def speed(self):
        return 5 + self.length / 3

    @property
    def velocity(self):
        return tuple(d * self.speed for d in self.direction)

    def death(self):
        destroy(self)
        btn = None
        def play_again():
            destroy(btn)
            self.__parent.loadSingleplayerGame()

        btn = Button('Play again?', position=(0,0), on_click=play_again)

    def input(self, key):
        print(key)
        old_direction = self.direction
        if key == 'w' or key == "up arrow":
            self.direction = (0, -1)
        if key == 'a' or key == "left arrow":
            self.direction = (1, 0)
        if key == 's' or key == "down arrow":
            self.direction = (0, 1)
        if key == 'd' or key == "right arrow":
            self.direction = (-1, 0)

        if(key.isnumeric()):
            self.skin = textures[int(key)]
            self.set_texture()
            for child in self.children:
                child.set_texture()

        if(old_direction[0] == -self.direction[0] or old_direction[1] == -self.direction[1] and not old_direction == (0, 0)):
            self.direction = old_direction
        else:
            self.actions.append(Action(self.direction, self.position))

        self.rotate_component()

    def update(self):
        self.update_children()
        self.x += self.velocity[0] * time.dt
        self.z += self.velocity[1] * time.dt
        self.check_collisions()

    def check_collisions(self):
        ceiling = Entity(model = 'quad', visible = False, scale = Vec3(50, 1, 1), position = (0, 0, -12), collider = 'box')
        floor = Entity(model = 'quad', visible = False, scale = Vec3(50, 1, 1), position = (0, 0, 12), collider = 'box')
        leftWall = Entity(model = 'quad', visible = False, scale = Vec3(1, 1, 50), position = (-22, 0, 0), collider = 'box')
        rightWall = Entity(model = 'quad', visible = False, scale = Vec3(1, 1, 50), position = (22, 0, 0), collider = 'box')
        for child in self.children[1:]:
            if (self.intersects(child)).hit and child.is_active:
                self.death()
                return
        if(self.intersects(ceiling)).hit:
            self.death()
        if(self.intersects(floor)).hit:
            self.death()
        if(self.intersects(leftWall)).hit:
            self.death()
        if(self.intersects(rightWall)).hit:
            self.death()
        if(self.intersects(food)).hit:
            food.relocate_apple()
            self.grow_snake()

    def update_children(self):
        delay = 0
        for idx, child in enumerate(self.children):
            delay += child.model_bounds.z / self.speed
            for action in self.actions:
                if(time.time() >= action.time + delay and not idx in action.completed_indices):
                    child.perform_action(action)
                    action.completed_indices.append(idx)

                    # Cleanup actions which have been exhausted
                    if(idx == len(self.children) - 1):
                        self.actions.remove(action)

            if(not child.is_active and time.time() >= child.activation_time):
                child.is_active = True

    def grow_snake(self):
        last_child = None
        if(len(self.children) == 0):
            last_child = self
        else:
            last_child = self.children[-1]
            last_child.tail = False

        child = SnakeBodyComponent(last_child.direction, self, tail = len(self.children) > 0)
        child.position = last_child.position
        child.position.y = child.model_bounds.y / 2

        if(not isinstance(last_child, Snake) and not last_child.is_active):
            child.activation_time = last_child.activation_time + last_child.model_bounds.z / self.speed
        else:
            child.activation_time = time.time() + last_child.model_bounds.z / self.speed
        self.children.append(child)

    @property
    def length(self):
        return len(self.children)

class SnakeBodyComponent(GenericSnakeComponent):
    def __init__(self, direction, parent, tail = True, activation_time = time.time()):
        super().__init__()
        self.tail = tail
        self._parent = parent
        self.set_texture()
        self.collider = 'box'
        self.direction = direction
        self.activation_time = activation_time
        self.is_active = False
        
    def set_texture(self):
        self.texture = 'assets/snakes/{0}/skin.jpg'.format(self._parent.skin)

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, value):
        if value:
            self.model = 'assets/snakes/tail.obj'
        else:
            self.model = 'assets/snakes/segment.obj'

    @property
    def velocity(self):
        return tuple(d * self._parent.speed for d in self.direction)

    def update(self):
        if(self.is_active):
            self.x += self.velocity[0] * time.dt
            self.z += self.velocity[1] * time.dt

    def perform_action(self, action):
        self.direction = action.direction
        self.position = action.position
