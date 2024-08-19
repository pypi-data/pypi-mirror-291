import math
from .events import PY_THUMBPAD_Directions

# Function to calculate angle in degrees from reference_coord to mouse position
def calculate_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    radians = math.atan2(dy, dx)
    degrees = math.degrees(radians)
    return degrees

def get_direction(angle):
    if angle == 0:
        return []

    if -135 <= angle < -45:
        return [ PY_THUMBPAD_Directions.TOP ]

    if  angle >= 135 or angle < -135:
        return [ PY_THUMBPAD_Directions.LEFT ]

    if -45 <= angle < 45:
        return [ PY_THUMBPAD_Directions.RIGHT ]

    if  45 <= angle < 135:
        return [ PY_THUMBPAD_Directions.BOTTOM ]
    
    return []

def get_direction_expanded(angle):
    if angle == 0:
        return []

    if -112.5 <= angle < -67.5:
        return [ PY_THUMBPAD_Directions.TOP ]

    if -157.5 <= angle < -112.5:
        return [ PY_THUMBPAD_Directions.TOP, PY_THUMBPAD_Directions.LEFT ]

    if -67.5 <= angle < -22.5:
        return [ PY_THUMBPAD_Directions.TOP, PY_THUMBPAD_Directions.RIGHT ]

    if 67.5 <= angle < 112.5:
        return [ PY_THUMBPAD_Directions.BOTTOM ]

    if 112.5 <= angle < 157.5:
        return [ PY_THUMBPAD_Directions.BOTTOM, PY_THUMBPAD_Directions.LEFT ]

    if 22.5 <= angle < 67.5:
        return [ PY_THUMBPAD_Directions.BOTTOM, PY_THUMBPAD_Directions.RIGHT ]

    if angle >= 157.5 or  angle < -157.5:
        return [ PY_THUMBPAD_Directions.LEFT ]
        
    if -22.5 <= angle < 22.5:
        return [ PY_THUMBPAD_Directions.RIGHT ]
    
    return []
