from ursina import *
import time

class Action():
    def __init__(self, direction, position):
        self.direction = direction
        self.position = position
        self.time = time.time()
        self.completed_indices = []

class SnakeComponent(Entity):
    def __init__(self, direction, parent, activation_time = time.time()):
        super().__init__()
        self.model='cube'
        self.collider = 'box'
        self.direction = direction
        self.activation_time = activation_time
        self.is_active = False
        self._parent = parent

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

class Snake(Entity):
    def __init__(self):
        super().__init__()
        self.model='cube'
        self.collider = 'box'
        self.color = color.black
        self.direction = (0, 0)
        self.position = (0, 0.5, 0)
        self.speed = 5                  # speed in units/s
        self.children = []
        self.actions = []

    @property
    def velocity(self):
        return tuple(d * self.speed for d in self.direction)

    def input(self, key):
        old_direction = self.direction
        if key == 'w' or key == "up_arrow":
            self.direction = (0, -1)
        if key == 'a' or key == "left_arrow":
            self.direction = (1, 0)
        if key == 's' or key == "down_arrow":
            self.direction = (0, 1)
        if key == 'd' or key == "right_arrow":
            self.direction = (-1, 0)

        if key == 'space':
          self.grow_snake()

        if(old_direction[0] == -self.direction[0] or old_direction[1] == -self.direction[1] and not old_direction == (0, 0)):
            self.direction = old_direction
        else:
            self.actions.append(Action(self.direction, self.position))

    def update(self):
        self.update_children()
        self.x += self.velocity[0] * time.dt
        self.z += self.velocity[1] * time.dt
        self.check_collisions()

    def check_collisions(self):
        for child in self.children[1:]:
            if(self.intersects(child)).hit:
                print("Hit")

    def update_children(self):
        delay = 0
        for idx, child in enumerate(self.children):
            delay += self.scale.x / self.speed
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
        child = SnakeComponent(last_child.direction, self)
        child.position = last_child.position
        if(not isinstance(last_child, Snake) and not last_child.is_active):
            child.activation_time = last_child.activation_time + last_child.scale.x / self.speed
        else:
            child.activation_time = time.time() + last_child.scale.x / self.speed
        self.children.append(child)

    @property
    def length(self):
        return len(self.children)