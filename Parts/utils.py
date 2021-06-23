def clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


def check_collisions(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    # x axis check
    if a_x + a_width >= b_x and a_x <= b_x + b_width:
        # y axis
        if a_y + a_height > b_y and a_y < b_y + b_height:
            return True
    return False
