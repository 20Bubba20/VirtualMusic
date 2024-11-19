import numpy as np
import cv2
from ui_objects import *


resolution = (500, 500)
button = UI_Element(
    x = 100,
    y = 100,
    draw_list=[
        UIShape('rectangle', (0,150,150), 0, 0, 100, 100, 5)
        # ,
        # UIText(10,0, 'This is Text', 2, (255, 255, 255), 4)
    ]
)

center = UI_Element(
    x = int(resolution[0]/2),
    y = int(resolution[1]/2),
    draw_list = [
        UIShape('ellipse', (255,255,255), -10, -10, 10, 10, 3)
    ]
)

print(center.x)
print(center.y)
dx, dy = (10, 15)
while True:
    # Create a black image
    img = np.full((resolution[0],resolution[1],3), 255, np.uint8)
    button.draw(img)
    center.draw(img)
    cv2.imshow("Test UI", img)
    # print(f'{button.size()}')
    # print(f'x: {button.x}; y: {button.y}')
    # print(f'dx: {dx}; dy: {dy}')
    # print(f'x_max: {button.x_max}; y_max: {button.y_max}')
    # print(f'x_min: {button.x_min}; y_min: {button.y_min}')
    
    button.change_position(button.x + dx, button.y + dy)
    if button.x_max >= resolution[0] or button.x_min <= 0:
        dx = dx * -1
        # button.change_position(button.x + dx*10, button.y)
        print("button change x direction")
    if button.y_max >= resolution[1] or button.y_min <= 0:
        dy = dy * -1
        # button.change_position(button.x, button.y + dy*10)
        print("button change y direction")
    if button.collision(center.x,center.y):
        print("In Center")
    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27:
        print('Exiting')
        cv2.destroyAllWindows()
        break
