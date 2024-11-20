import numpy as np
import cv2
from ui_objects import *

scale = (16, 9)
k = 80
resolution = (k*scale[0],k*scale[1]) #(1280, 720)
# print(resolution)
PrimaryColor = (132, 96, 18)
TitleBig = UI_Element(
    name = 'title',
    x = 325,
    y = 200,
    draw_list=[
        UIText((0, 0, 0), 0, 0, 'Virtual Music', 2, 4),
        UIEllipse((0,0,0), 0, 0, 3, 3, -1)
    ]
)

PracticeButton = UI_Element(
    name = 'practice',
    x = 300,
    y = 205,
    draw_list=[
        UIRect(PrimaryColor, 0,0, 160, 45, -1),
        # UIRect((0,0,0), 0,0, 160, 45, 1),
        UIText((255,255,255), 5, 55, 'Practice', 1, 2)
    ]
)


HomeScene = Scene(
    name = 'home',
    elements=[
        TitleBig,
        PracticeButton
    ]
)

element_dots = [
    UI_Element(
    name = f'({shift_x},{shift_y})',
    x = shift_x,
    y = shift_y,
    draw_list=[
        UIEllipse(
            color=PrimaryColor,
            dx=0,
            dy=0,
            dx_size=2,
            dy_size=3,
            thickness=-1
        ),
        UIText(
            color=(0,0,0),
            dx=0,
            dy=0,
            text= f'({shift_x},{shift_y})',
            scale=1,
            thickness=1
        )
     ]) for shift_x in range(0, resolution[0], int(resolution[0]/5)) for shift_y in range(0, resolution[1], int(resolution[0]/5))
]

shape_dots = [
    UI_Element(
    name = f'({shift_x},{shift_y})',
    x = 0,
    y = 0,
    draw_list=[
        UIEllipse(
            color=PrimaryColor,
            dx=shift_x,
            dy=shift_y,
            dx_size=shift_x+2,
            dy_size=shift_y+3,
            thickness=-1
        ),
        UIText(
            color=(0,0,0),
            dx=shift_x,
            dy=shift_y,
            text= f'({shift_x},{shift_y})',
            scale=1,
            thickness=1
        )
     ]) for shift_x in range(0, resolution[0], int(resolution[0]/5)) for shift_y in range(0, resolution[1], int(resolution[0]/5))
]

element_scene = Scene(
    name = 'element scene',
    elements=element_dots
)
shape_scene = Scene(
    name = 'shape scene',
    elements=shape_dots
)

toggle = True

while True:
    # Create a white image
    img = np.full((resolution[1],resolution[0],3), 255, np.uint8)
    # HomeScene.render(img)
    if toggle:
        print('By Element')
        element_scene.render(img)
    else:
        print('By Shape')
        shape_scene.render(img)
        
    HomeScene.render(img)
    cv2.imshow("Test UI", img)
    
    if cv2.waitKey(-1) == ord('q') or cv2.waitKey(-1) == 27:
        print('Exiting')
        cv2.destroyAllWindows()
        break
    toggle = not toggle
    print('Switching')
