def rectangle_contains(x1, y1, width1, height1, x2, y2, width2, height2):
    return x2 >= x1 and x2 + width2 <= x1 + width1 and y2 >= y1 and y2 + height2 <= y1 + height1

def rectangles_intersect(x1, y1, width1, height1, x2, y2, width2, height2):
    return x1 + width1 > x2 and x2 + width2 > x1 and y1 + height1 > y2 and y2 + height2 > y1
