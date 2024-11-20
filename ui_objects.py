import cv2 as cv
from math import sin, cos, sqrt, pi

class UIShape:
    def __init__(self, type: str, color: tuple[int, int, int], dx: int, dy: int, thickness: int):
        self.dx = dx
        self.dy = dy
        self.type = type
        self.color = color
        self.thickness = thickness
        self.range()
        
    def draw(self, img, parent_pos):
        match self.type:
                case 'line':
                    cv.line(img, (parent_pos[0] + self.dx_start, parent_pos[0] + self.dy_start), (parent_pos[0] + self.dx_end, parent_pos[0] + self.dy_end), self.color, self.border)
                case 'rectangle':
                    cv.rectangle(img, (parent_pos[0] + self.dx_start, parent_pos[0] + self.dy_start), (parent_pos[0] + self.dx_end, parent_pos[0] + self.dy_end), self.color, self.border)
                case 'ellipse':
                    center = (int((self.dx_end + self.dx_start)/2) + parent_pos[0], int((self.dy_end + self.dy_start)/2) + parent_pos[0])
                    axis = (
                        abs(self.dx_end - self.dx_start),
                        abs(self.dy_end - self.dy_start)
                    )
                    cv.ellipse(img, center, axis, self.angle, self.start_angle, self.end_angle, self.color, thickness=self.border)
                case 'text':
                    cv.putText(img, self.text, (parent_pos[0] + self.dx, parent_pos[0] + self.dy), self.font, self.font_size, self.color, self.thickness, cv.LINE_AA)
    def range(self):
        x_max = -10000
        x_min = 10000
        y_max = -10000
        y_min = 10000
        if self.type == 'text':
            if self.dx < x_min:
                x_min = self.dx
            if self.dy < y_min:
                y_min = self.dy

        if self.type == 'elipse':
            center = (self.x + self.dx_start, self.y + self.dy_start)
            r1 = self.dx_end
            r2 = self.dy_end
            angle = self.angle

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

        if self.dx_start < x_min:
            x_min = self.dx_start
        if self.dy_start < y_min:
            y_min = self.dy_start
        if self.dx_start > x_max:
            x_max = self.dx_start
        if self.dy_start > y_max:
            y_max = self.dy_start
            
        if self.dx_end < x_min:
            x_min = self.dx_end
        if self.dy_end < y_min:
            y_min = self.dy_end
        if self.dx_end > x_max:
            x_max = self.dx_end
        if self.dy_end > y_max:
            y_max = self.dy_end
        pass
        
class UIEllipse(UIShape):
    def __init__(self, name: str, color: tuple[int, int, int], dx: int, dy: int, dx_size: int, dy_size: int, thickness: int, angle: float = 0, start_angle: float = 0, end_angle: float = 360):
        self.name = name
        self.dx_size = dx_size
        self.dy_size = dy_size
        self.angle = angle
        self.start_angle = start_angle
        self.end_angle = end_angle
        super().__init__('ellipse', color, dx, dy, thickness)
        
    def draw(self,img, parent_pos):
        center = (int((self.dx_size + self.dx)/2) + parent_pos[0], int((self.dy_end + self.dy_start)/2) + parent_pos[0])
        axis = (
            abs(self.dx_size - self.dx),
            abs(self.dy_size - self.dy)
        )
        cv.ellipse(img, center, axis, self.angle, self.start_angle, self.end_angle, self.color, thickness=self.border)
        
    def range(self):
        center = (self.x + self.dx_start, self.y + self.dy_start)
        r1 = self.dx_end
        r2 = self.dy_end
        angle = self.angle

        ux = r1 * cos(angle)
        uy = r1 * sin(angle)
        vx = r2 * cos(angle + pi/2)
        vy = r2 * sin(angle + pi/2)

        bbox_halfwidth = sqrt(ux*ux + vx*vx)
        bbox_halfheight = sqrt(uy*uy + vy*vy)

        
        self.min_x= center.x - bbox_halfwidth
        self.min_y= center.y - bbox_halfheight
        self.max_x= center.x + bbox_halfwidth 
        self.max_y= center.y + bbox_halfheight

class UIRect(UIShape):
    def __init__(self, color: tuple[int, int, int], dx_start: int, dy_start: int, dx_end: int, dy_end: int, thickness: int):
        self.dx_end = dx_end
        self.dy_end = dy_end
        super().__init__('rectangle', color, dx_start, dy_start, thickness)
        
    def draw(self, img, parent_pos):
        cv.rectangle(img, (parent_pos[0] + self.dx_start, parent_pos[0] + self.dy_start), (parent_pos[0] + self.dx_end, parent_pos[0] + self.dy_end), self.color, self.border)
        
    def range(self):
        self.min_x= min(self.dx,self.dx_end)
        self.min_y= min(self.dy,self.dy_end)
        self.max_x= max(self.dx,self.dx_end)
        self.max_y= max(self.dy,self.dy_end)
        
class UILine(UIRect):
    def __init__(self, color, dx_start, dy_start, dx_end, dy_end, thickness):
        super().__init__(color, dx_start, dy_start, dx_end, dy_end, thickness)
        self.type = 'line'
        
    def draw(self, img, parent_pos):
        cv.line(img, (parent_pos[0] + self.dx, parent_pos[0] + self.dy), (parent_pos[0] + self.dx_end, parent_pos[0] + self.dy_end), self.color, self.thickness)
                
        

class UIText(UIShape):
    def __init__(self, color, dx, dy, text, scale, thickness):
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
    def __init__(self, x: int, y: int, draw_list: list[UIShape]):
        self.x: int = x
        self.y: int = y
        self.draw_list = draw_list
        self.range()
        self.set_font()
    
    def range(self):
        x_max = max([shape.x_max for shape in self.draw_list])
        x_min = min([shape.x_min for shape in self.draw_list])
        y_max = max([shape.y_max for shape in self.draw_list])
        y_min = min([shape.y_min for shape in self.draw_list])
        
        self.x_max = x_max + self.x
        self.x_min = x_min + self.x
        self.y_max = y_max + self.y
        self.y_min = y_min + self.y
        pass
        
    def size(self):
        return (self.x_max - self.x_min, self.y_max - self.y_min)
    
    def draw(self, img):
        for shape in self.draw_list:
            shape.draw(img,(self.x, self.y))
        pass
    
    def set_font(self, font = cv.FONT_HERSHEY_SIMPLEX):
        self.font = font
        
    
    def collision(self, point_x, point_y):
        return (point_x <= self.x_max and point_x >= self.x_min) and (point_y <= self.y_max and point_y >= self.y_min)
    
    def change_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.range()