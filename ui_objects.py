import cv2
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
                    cv2.line(img, (parent_pos[0] + self.dx_start, parent_pos[0] + self.dy_start), (parent_pos[0] + self.dx_end, parent_pos[0] + self.dy_end), self.color, self.border)
                case 'rectangle':
                    cv2.rectangle(img, (parent_pos[0] + self.dx_start, parent_pos[0] + self.dy_start),
                                  (parent_pos[0] + self.dx_end, parent_pos[0] + self.dy_end), self.color, self.border)
                case 'ellipse':
                    center = (int((self.dx_end + self.dx_start)/2) + parent_pos[0],
                              int((self.dy_end + self.dy_start)/2) + parent_pos[0])

                    axis = (abs(self.dx_end - self.dx_start),
                            abs(self.dy_end - self.dy_start))

                    cv2.ellipse(img, center, axis, self.angle, self.start_angle, self.end_angle,
                                self.color, thickness=self.border)
                case 'text':
                    cv2.putText(img, self.text, (parent_pos[0] + self.dx, parent_pos[1] + self.dy),
                                self.font, self.font_size, self.color, self.thickness, cv2.LINE_AA)
    def range(self):
        x_max = -10000
        x_min = 10000
        y_max = -10000
        y_min = 10000

        if self.type == 'text':
            self.x_max = self.dx
            self.x_min = self.dx
            self.y_max = self.dy
            self.y_min = self.dy

        elif self.type == 'ellipse':
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

            self.x_min = min(minx, x_min)
            self.y_min = min(miny, y_min)
            self.x_max = max(maxx, x_max)
            self.y_max = max(maxy, y_max)

        else:
            self.x_max = max(x_max, self.dx, self.dx_start, self.dx_end)
            self.x_min = min(x_min, self.dx, self.dx_start, self.dx_end)
            self.y_max = max(y_max, self.dy, self.dy_start, self.dy_end)
            self.y_min = min(y_min, self.dy, self.dy_start, self.dy_end)

        pass
        
class UIEllipse(UIShape):
    def __init__(self, color: tuple[int, int, int], dx: int, dy: int, dx_size: int, dy_size: int,
                 thickness: int, angle: float = 0, start_angle: float = 0, end_angle: float = 360):
        self.dx_size = dx_size
        self.dy_size = dy_size
        self.angle = angle
        self.start_angle = start_angle
        self.end_angle = end_angle
        super().__init__('ellipse', color, dx, dy, thickness)
        self.range()

    def draw(self,img, parent_pos):
        center = (int((self.dx_size + self.dx)/2) + parent_pos[0], int((self.dy_size + self.dy)/2) + parent_pos[0])
        axis = (
            abs(self.dx_size - self.dx),
            abs(self.dy_size - self.dy)
        )
        cv2.ellipse(img, center, axis, self.angle, self.start_angle, self.end_angle,
                    self.color, thickness=self.thickness)
        # print(f'Ellipse from ({self.dx+parent_pos[0]}, {self.dy+parent_pos[1]}) to \
        # ({self.dx_size+parent_pos[0]}, {self.dy_size+parent_pos[1]})')
        
    def range(self):
        center = ((self.dx + self.dx_size)/2, (self.dy + self.dy_size)/2)
        r1 = self.dx_size
        r2 = self.dy_size
        angle = self.angle

        ux = r1 * cos(angle)
        uy = r1 * sin(angle)
        vx = r2 * cos(angle + pi/2)
        vy = r2 * sin(angle + pi/2)

        bbox_halfwidth = sqrt(ux*ux + vx*vx)
        bbox_halfheight = sqrt(uy*uy + vy*vy)

        
        self.x_min = int(center[0] - bbox_halfwidth)
        self.y_min = int(center[1] - bbox_halfheight)
        self.x_max = int(center[0] + bbox_halfwidth)
        self.y_max = int(center[1] + bbox_halfheight)

class UIRect(UIShape):
    def __init__(self, color: tuple[int, int, int], dx_start: int, dy_start: int,
                 dx_end: int, dy_end: int, thickness: int):
        self.dx_end = dx_end
        self.dy_end = dy_end
        self.dx_start = dx_start
        self.dy_start = dy_start
        super().__init__('rectangle', color, dx_start, dy_start, thickness)
        
    def draw(self, img, parent_pos):
        cv2.rectangle(img, ((parent_pos[0] + self.x_min), (parent_pos[1] + self.y_min)),
                      ((parent_pos[0] + self.x_max), (parent_pos[1] + self.y_max)), self.color, self.thickness)
        # print(f'Rectangle from ({self.x_min+parent_pos[0]}, {self.y_min+parent_pos[1]}) to \
        # ({self.x_max+parent_pos[0]}, {self.y_max+parent_pos[1]})')
        
class UILine(UIRect):
    def __init__(self, color, dx_start, dy_start, dx_end, dy_end, thickness):
        super().__init__(color, dx_start, dy_start, dx_end, dy_end, thickness)
        self.type = 'line'
        
    def draw(self, img, parent_pos):
        cv2.line(img, (parent_pos[0] + self.dx, parent_pos[0] + self.dy),
                 (parent_pos[0] + self.dx_end, parent_pos[0] + self.dy_end), self.color, self.thickness)
        # print(f'Line from ({self.dx+parent_pos[0]}, {self.dy+parent_pos[1]}) to \
        # ({self.dx_end+parent_pos[0]}, {self.dy_end+parent_pos[1]})')

class UIText(UIShape):
    def __init__(self, color, dx, dy, text, scale, thickness ):
        self.dx, self.x_max, self.x_min = (dx,dx,dx)
        self.dy, self.y_max, self.y_min = (dy,dy,dy)
        self.text = text
        self.font_size = scale
        self.color = color
        self.thickness = thickness
        self.set_font()
        pass
    
    def set_font(self, font = cv2.FONT_HERSHEY_SIMPLEX):
        self.font = font
        
    def draw(self, img, parent_pos):
        cv2.putText(img, self.text, ((parent_pos[0] + self.dx), (parent_pos[1] + self.dy)),
                    self.font, self.font_size, self.color, self.thickness, cv2.LINE_AA)
        # print(f'Text at {(parent_pos[0] + self.dx, parent_pos[1] + self.dy)}')
    pass 

class UI_Element:
    def __init__(self, name:str, x: int, y: int, draw_list: list[UIShape]):
        self.name = name
        self.x=int(x)
        self.y=int(y)
        self.draw_list = draw_list
        self.range()
    
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
        return self.x_max - self.x_min, self.y_max - self.y_min
    
    def draw(self, img):
        # print(f'{self.name} ({self.x, self.y}):')
        for shape in self.draw_list:
            shape.draw(img,(self.x, self.y))

        pass

    def check_within(self, point_x, point_y):
        return (self.x_max >= point_x >= self.x_min) and (self.y_max >= point_y >= self.y_min)
    
    def change_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.range()
    
    def check_collision(self, other):
        return (
            ((self.x_min <= other.x_max <= self.x_max) and (self.y_min <= other.y_max <= self.y_max))
            or
            ((self.x_min <= other.x_min <= self.x_max) and (self.y_min <= other.y_min <= self.y_max))
        )
    
    def set_font(self, font):
        for element in self.draw_list:
            if element.type == 'text':
                element.set_font(font)
        
class Scene:
    def __init__(self, name, elements: list[UI_Element]):
        self.name = name
        self.contents = elements
        self.scene_start = 0
        pass
    
    def render(self, background):
        for element in self.contents:
            element.draw(background)
            
    def check_points(self, point_list: list[tuple[int, int]]) -> list[str]:
            
        selected = []
        for element in self.contents:
            for point in point_list:
                if element.name in selected:
                    break
                if element.check_within(point[0],point[1]):
                    selected.append(element.name)
                
        return selected
        pass