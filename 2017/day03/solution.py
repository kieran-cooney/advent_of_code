"""
Throughout the solution we assume square 1 is at (0, 0) and the orientation
is as in the problem page.
"""
from math import sqrt, floor
INPUT = 361527


def get_grid_coords_square_corner(side_length):
    """
    Get the coordinates of the last number (side_length^2) when the spiral
    so far is a perfect square.
    """
    assert side_length > 0, "side_length must be positive"
    
    if side_length % 2 == 0:
        offset = (side_length)//2
        return (1-offset, offset)
    else:
        offset = (side_length - 1)//2
        return (offset, -offset)
        
    
def get_grid_coords(i):
    """
    Get the coordinates for an aribtrary number
    """
    # Find the coordinates of the last square number, and figure out
    # how much is left
    side_length = floor(sqrt(i))
    corner_x, corner_y = get_grid_coords_square_corner(side_length)
    leftover = i - (side_length)**2

    # The next numbers wrap around in different directions if the last square
    # number was odd or even. The direction variable takes care of this
    # annoying logic
    direction = 1 if (side_length % 2 == 1) else -1

    # Need to go through different cases if the leftover makes it to a new,
    # non-square corner.
    if leftover == 0:
        # Easy
        return (corner_x, corner_y)
    elif leftover <= side_length + 1:
        # Wrap around the square from the corner.
        return (corner_x + direction, corner_y + direction*(leftover - 1))
    else:
        # Now we hit another corner, so make a new leftover.
        leftover = leftover - side_length
        # Wrap around some more. There's no great elegance to these formulae,
        # they just work.
        return (corner_x + direction*(2 - leftover), corner_y + direction*side_length)


def get_steps_to_access_port(i):
    x, y = get_grid_coords(i)
    return abs(x) + abs(y)

print(get_steps_to_access_port(INPUT))