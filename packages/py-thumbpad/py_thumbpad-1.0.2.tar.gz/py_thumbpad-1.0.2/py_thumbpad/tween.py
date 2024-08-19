import pygame

# Easing functions
def ease_in_out(t):
    return t * t * (3 - 2 * t)

def ease_in(t):
    return t * t

def ease_out(t):
    return t * (2 - t)

def linear(t):
    return t

easing_fns = {
    'ease_in_out': ease_in_out,
    'ease_in': ease_in,
    'ease_out': ease_out,
    'linear': linear
}

class Tween:
    def __init__(self, obj, attr, start_value, end_value, duration, animation) -> None:
        self.obj = obj
        self.attr = attr
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.animation = easing_fns[animation]
        self.start_time = None
        self.current = self.start
        self.is_complete = False

    def start(self):
        self.start_time = pygame.time.get_ticks() / 1000
    
    def update(self):
        if self.start_time is None:
            return

        current_time = pygame.time.get_ticks() / 1000
        elapsed_time = current_time - self.start_time
        t = min(elapsed_time / self.duration, 1)
        eased_t = self.animation(t)
        current_value = self.interpolate(self.start_value, self.end_value, eased_t)
        setattr(self.obj, self.attr, current_value)

        if t >= 1:
            self.is_complete = True

    def interpolate(self, starts, ends, eased_t):
        return starts + eased_t * (ends - starts)

    @classmethod
    def animate(cls, obj, attr, start_value, end_value, duration, animation):
        tween_instance = cls(obj, attr, start_value, end_value, duration, animation)
        tween_instance.start()
        return tween_instance
    