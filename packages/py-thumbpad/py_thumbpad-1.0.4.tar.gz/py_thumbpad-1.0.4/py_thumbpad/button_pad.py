import pygame 
import math
from py_thumbpad.tween import Tween

def distance(point_1, point_2):
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

class ButtonPad:
    def __init__(self, position, radius, color):
        self.position = position
        self.radius = radius
        self.color = color
        self.dragging = False
        self.animations = []
        self.track_touches = []
        self.setup()

    def setup(self):
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.x = self.position[0] - self.radius
        self.rect.y = self.position[1] - self.radius
        self.initial_position = [self.rect.x, self.rect.y]

    def listen_events(self, event, donut): 
        mouse_pos = pygame.mouse.get_pos()
        # Check if the click is inside the circle
        distance_between_mouse_and_button = distance(mouse_pos, [self.rect.x + self.radius, self.rect.y + self.radius])
        # is the button down
        is_button_down = event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN
        is_button_up = event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP

        if is_button_down and distance_between_mouse_and_button > donut.outer_radius:
            self.track_touches.append(0)

        if is_button_down and distance_between_mouse_and_button < donut.outer_radius:
            self.dragging = True
            if 1 in self.track_touches:
                self.track_touches.append(0)
                return
            self.track_touches.append(1)

        if is_button_up:
            if len(self.track_touches) > 0 and self.track_touches[len(self.track_touches) - 1] == 0:
                for item in self.track_touches:
                    if item == 0:
                        self.track_touches.remove(item)
                return
            if len(self.track_touches) > 0 and self.track_touches[0] == 1:
                self.dragging = False
                self.return_back()
            self.track_touches = []

        if self.dragging:
            self.update_position(mouse_pos, donut)

    def return_back(self):
        from_x = self.rect.x
        from_y = self.rect.y
        duration = 0.3
        self.animations = [
            Tween.animate(self.rect, 'x', from_x, self.initial_position[0], duration, 'ease_in_out'),
            Tween.animate(self.rect, 'y', from_y, self.initial_position[1], duration, 'ease_in_out')
        ]

    def update_position(self, mouse_pos, donut):
        dist_to_center = distance(mouse_pos, donut.position)

        # Ensure the small circle stays within the container
        if dist_to_center + self.radius <= donut.outer_radius:
            self.rect.x = mouse_pos[0]
            self.rect.y = mouse_pos[1]
        
        if dist_to_center + self.radius > donut.outer_radius:
            angle = math.atan2(mouse_pos[1] - donut.position[1], mouse_pos[0] - donut.position[0])
            self.rect.x = donut.position[0] + ( donut.outer_radius - self.radius ) * math.cos(angle) 
            self.rect.y = donut.position[1] + ( donut.outer_radius - self.radius ) * math.sin(angle) 

        self.rect.x = self.rect.x - self.radius
        self.rect.y = self.rect.y - self.radius

    def update(self):
        for animation in self.animations:
            animation.update()

        self.animations = [animation for animation in self.animations if not animation.is_complete]

    def render(self, screen):
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)
        screen.blit(self.surface, (self.rect.x, self.rect.y))
