import pygame
from .donut import Donut
from .button_pad import ButtonPad
from .utils import calculate_angle, get_direction, get_direction_expanded
from .events import PY_THUMBPAD_Directions

# to export the enum of the custom events
__all__ = ['PY_THUMBPAD_Directions']

class PyThumbPad:
    def __init__(self, position, options):
        defaults = {
            "quadrants": 4,
            "donut_color": (123, 157, 243),
            "button_color": (255, 255, 0),
            "donut_bg_color": (0, 0, 0)
        }
        settings = defaults.copy()
        settings.update(options)
        self.donut_outer_radius = 125
        self.donut_inner_radius = 120
        self.position = position
        self.button_radius = 75
        self.donut = Donut(self.position, self.donut_outer_radius, self.donut_inner_radius, settings["donut_color"], settings["donut_bg_color"])
        self.button_pad = ButtonPad(self.position, self.button_radius, settings["button_color"]) 
        self.current_angle = 0.0
        self.quadrants = settings["quadrants"]
        self.directions = []

    def update(self):
        self.button_pad.update()

    def render(self, screen):
        self.donut.render(screen)
        self.button_pad.render(screen)

    def listen_events(self, event):
        self.button_pad.listen_events(event, self.donut)
        self.directions = self.get_directions(0)
        self.current_angle = 0.0
        if self.button_pad.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.current_angle = calculate_angle(self.position[0], self.position[1], mouse_x, mouse_y )
            self.directions = self.get_directions(self.current_angle)
    
    def get_directions(self, current_angle):
        if self.quadrants == 4:
            return get_direction(current_angle)
        return get_direction_expanded(current_angle)

