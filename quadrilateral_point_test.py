def check_if_point_is_inside_quadrilateral(iter_of_points, point_to_check):
    """Check if point is inside a quadrilateral. 
    NOTE: Only tested with a square rhomboid, may not work with any quadrilateral.
        @param iterable of points
        @param tuple
        @return True=point is inside shape. False=point is outside shape.
    """
    # Divide quadrilaterial into 2 triangles
    x_sorted = sorted(iter_of_points, key=lambda point: point[0]) # sort w/ respect to x-component
    left_triangle = x_sorted[0:3]
    right_triangle = x_sorted[1:4]

    def left_segments_check(iter_of_points):
        """
        Check if point is in left triangle.
            @param points of left triangle
            @return bool: True=point is in triangle False=point is not in triangle
        """
        y_sorted = sorted(x_sorted[0:3], key=lambda point: point[1])
        bottomleft_segment = y_sorted[0:2]
        topleft_segment = y_sorted[1:3]
        
        """Bottomleft"""
        # below and to right (greater y val, greater x val)
        above_bool_1, right_bool_1 = get_above_and_to_right_checks(*bottomleft_segment, point_to_check)
        if above_bool_1 and right_bool_1:
            condition_1 = True
        else:
            condition_1 = False
        
        """Topleft"""
        # above and to right (smaller y val, greater x val)
        above_bool_2, right_bool_2 = get_above_and_to_right_checks(*topleft_segment, point_to_check)
        if not above_bool_2 and right_bool_2:
            condition_2 = True
        else: 
            condition_2 = False
        if condition_1 and condition_2:
            return True
        else:
            return False

    def right_segments_check(iter_of_points):
        """
        Check if point is in left triangle.
            @param points of left triangle
            @return bool: True=point is in triangle False=point is not in triangle
        """
        p_1, p_2, p_3 = iter_of_points[:]
        p_1, p_2 = sort_y(p_1, p_2)
        bottomright_segment = [p_1, p_3]
        topright_segment = [p_2, p_3]
        
        """Bottomright"""
        # above and to left (greater y val, smaller x val)
        above_bool_1, right_bool_1 = get_above_and_to_right_checks(*bottomright_segment, point_to_check)
        if above_bool_1 and not right_bool_1:
            condition_1 = True
        else:
            condition_1 = False

        """Topright"""
        # below and to left (smaller y val, smaller x val)
        above_bool_2, right_bool_2 = get_above_and_to_right_checks(*topright_segment, point_to_check)
        if not above_bool_2 and not right_bool_2:
            condition_2 = True
        else: 
            condition_2 = False
        if condition_1 and condition_2:
            return True
        else:
            return False
    
    if len(iter_of_points) != 4:
        raise ValueError("Number of points must equal 4.")
    in_left_triangle = left_segments_check(left_triangle)
    in_right_triangle = right_segments_check(right_triangle)
    if in_left_triangle and in_right_triangle:
        # point is in shape
        return True
    else:
        # point is not in shape
        return False

def get_above_and_to_right_checks(point_1, point_2, point_to_check):
    """
    Get booleans of if point is above and to the right of a given line segment.
        @param 2-tuple
        @param 2-tuple
        @param 2-tuple
        @return bool: above line segment
        @return bool: to right of line segment
    """
    above_bool = check_if_point_is_above_line_segment(point_1, point_2, point_to_check)
    right_bool = check_if_point_is_to_the_right_of_line_segment(point_1, point_2, point_to_check)
    return above_bool, right_bool

def check_if_point_is_above_line_segment(point_1, point_2, point_to_check):
    """
    Get booleans of if point is above a given line segment.
        @param 2-tuple
        @param 2-tuple
        @param 2-tuple
        @return bool: above line segment
    """
    point_to_check_x, point_to_check_y = point_to_check[:]
    slope = get_slope(point_1, point_2)
    if slope is None:
        # line segment is horizontal
        y_val = point_2[0]
    else:
        y_val = get_y_val(slope, point_2, point_to_check_x)

    if point_to_check_y > y_val: # >=
        # point is above line segment
        return True
    else:
        # point is below line segment
        return False

def check_if_point_is_to_the_right_of_line_segment(point_1, point_2, point_to_check):
    """
    Get booleans of if point is to the right of a given line segment.
        @param 2-tuple
        @param 2-tuple
        @param 2-tuple
        @return bool: to right of line segment
    """
    point_to_check_x, point_to_check_y = point_to_check[:]
    slope = get_slope(point_1, point_2)
    if slope is None or slope == 0:
        # line segment is horizontal
        point_1, point_2 = sort_x(point_1, point_2)
        x_val = point_1[0]
        if point_to_check_x >= x_val: # >=
            # point is to the right of line segment
            return True
        else:
            return False
    else:
        x_val = get_x_val(slope, point_2, point_to_check_y)
        if point_to_check_x > x_val: # >=
            # point is above line segment
            return True
        else:
            return False


def sort_x(point_1, point_2):
    """
    Sort the points in ascending order with respect to the x-component.
        @param tuple
        @param tuple
        @return sorted tuples
    """
    if point_1[0] > point_2[0]:
        return point_2, point_1
    else:
        return point_1, point_2

def sort_y(point_1, point_2):
    """
    Sort the points in ascending order with respect to the y-component.
        @param tuple
        @param tuple
        @return sorted tuples
    """
    if point_1[1] > point_2[1]:
        return point_2, point_1
    else:
        return point_1, point_2

def get_x_val(slope, point, y_val):
    """Get x value using point slope formula.
        @param int
        @param 2-tuple
        @param int
        @return x value = int
    """
    # (y-y_1) / m + x_1 = x
    x_1, y_1 = point[:]
    if slope == 0:
        # x is infinite
        return None
    else:
        return ((y_val - y_1)/slope) + x_1

def get_y_val(slope, point, x_val):
    """Get y value using point slope formula.
        @param int
        @param 2-tuple
        @param int
        @return y value = int
    """
    # y = m(x-x_1) + y_1
    x_1, y_1 = point[:]
    return slope*(x_val - x_1) + y_1

def get_slope(point_1, point_2):
    """Get the slope of the line between the two points.
        @param 2-tuple
        @param 2-tuple
        @return int or None: slope or slope is infinite
    """
    x_1, y_1 = point_1[:]
    x_2, y_2 = point_2[:]
    denominator = y_2 - y_1
    if denominator == 0:
        # slope is infinite
        # line is horizontal
        return None
    else:
        numerator = x_2 - x_1
        return numerator/denominator
