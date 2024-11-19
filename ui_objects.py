import cv2 as cv
from math import sin, cos, sqrt, pi

class UIShape:
    def __init__(self, type: str, color: tuple[int, int, int], dx_start: int, dy_start: int, dx_end: int, dy_end: int, thickness: int, angle: float = None, start_angle: float = None, end_angle: float = None):
        self.dx_start = dx_start
        self.dy_start = dy_start
        self.dx_end = dx_end
        self.dy_end = dy_end
        self.border = thickness
        self.color = color
        self.type = type
        if type == 'ellipse':
            if start_angle is None or end_angle is None:
                start_angle = 0
                end_angle = 360
            if angle is None:
                angle = 0
        self.angle = angle
        self.start_angle = start_angle
        self.end_angle = end_angle
        

class UIText:
    def __init__(self, dx, dy, text, scale, color, thickness):
        self.dx = dx
        self.dy = dy
        self.text = text
        self.font_size = scale
        self.color = color
        self.thickness = thickness
        self.type = 'text'
        pass
    pass 

class UI_Element:
    def __init__(self, x: int, y: int, draw_list: list[UIShape | UIText]):
        self.x: int = x
        self.y: int = y
        self.draw_list = draw_list
        self.range()
        self.set_font()
    
    def range(self):
        x_max = -10000
        x_min = 10000
        y_max = -10000
        y_min = 10000
        for shape in self.draw_list:
            if shape.type == 'text':
                if shape.dx < x_min:
                    x_min = shape.dx
                if shape.dy < y_min:
                    y_min = shape.dy
                continue
            
            if shape.type == 'elipse':
                center = (self.x + shape.dx_start, self.y + shape.dy_start)
                r1 = shape.dx_end
                r2 = shape.dy_end
                angle = shape.angle

                ux = r1 * cos(angle)
                uy = r1 * sin(angle)
                vx = r2 * cos(angle + pi/2)
                vy = r2 * sin(angle + pi/2)

                bbox_halfwidth = sqrt(ux*ux + vx*vx)
                bbox_halfheight = sqrt(uy*uy + vy*vy)

                
                minx= center.x - bbox_halfwidth
                miny= center.y - bbox_halfheight
                maxx= center.x + bbox_halfwidth 
                maxy= center.y + bbox_halfheight
                if minx < x_min:
                    x_min = minx
                if miny < y_min:
                    y_min = miny
                if maxx > x_max:
                    x_min = maxx
                if maxy > y_max:
                    y_min = maxy
                continue
            
            if shape.dx_start < x_min:
                x_min = shape.dx_start
            if shape.dy_start < y_min:
                y_min = shape.dy_start
            if shape.dx_start > x_max:
                x_max = shape.dx_start
            if shape.dy_start > y_max:
                y_max = shape.dy_start
                
            if shape.dx_end < x_min:
                x_min = shape.dx_end
            if shape.dy_end < y_min:
                y_min = shape.dy_end
            if shape.dx_end > x_max:
                x_max = shape.dx_end
            if shape.dy_end > y_max:
                y_max = shape.dy_end
            pass
        
        self.x_max = x_max + self.x
        self.x_min = x_min + self.x
        self.y_max = y_max + self.y
        self.y_min = y_min + self.y
        pass
        
    def size(self):
        return (self.x_max - self.x_min, self.y_max - self.y_min)
    
    def draw(self, img):
        for shape in self.draw_list:
            match shape.type:
                case 'line':
                    cv.line(img, (self.x + shape.dx_start, self.y + shape.dy_start), (self.x + shape.dx_end, self.y + shape.dy_end), shape.color, shape.border)
                case 'rectangle':
                    cv.rectangle(img, (self.x + shape.dx_start, self.y + shape.dy_start), (self.x + shape.dx_end, self.y + shape.dy_end), shape.color, shape.border)
                case 'ellipse':
                    center = (int((shape.dx_end + shape.dx_start)/2) + self.x, int((shape.dy_end + shape.dy_start)/2) + self.y)
                    axis = (
                        abs(shape.dx_end - shape.dx_start),
                        abs(shape.dy_end - shape.dy_start)
                    )
                    cv.ellipse(img, center, axis, shape.angle, shape.start_angle, shape.end_angle, shape.color, thickness=shape.border)
                case 'text':
                    cv.putText(img, shape.text, (self.x + shape.dx, self.y + shape.dy), self.font, shape.font_size, shape.color, shape.thickness, cv.LINE_AA)
            pass
        pass
    
    def set_font(self, font = cv.FONT_HERSHEY_SIMPLEX):
        self.font = font
        
    
    def collision(self, point_x, point_y):
        return (point_x <= self.x_max and point_x >= self.x_min) and (point_y <= self.y_max and point_y >= self.y_min)
    
    def change_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.range()