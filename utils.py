def clamp(value, min_, max_):
    if value < min_:
        return min_
    if value > max_:
        return max_
    return value


def check_collisions(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    return (a_x + a_width > b_x) and (a_x < b_x + b_width) and (a_y + a_height > b_y) and (a_y < b_y + b_height)
