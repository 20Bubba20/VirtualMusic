import numpy as np
import cv2
from ui_objects import *

scale = (16, 9)
k = 80
resolution = (k*scale[0],k*scale[1]) #(1280, 720)
# print(resolution)
PrimaryColor = (132, 96, 18)
White = (255, 255, 255)
Black = (0, 0, 0)

TitleBig = UI_Element(
    name = 'title',
    x = int(resolution[0] / 2 - 200),
    y = 200,
    draw_list=[
        UIText((0, 0, 0), 0, 0, 'Virtual Music', 2, 4)
    ]
)

TitleSmall = UI_Element(
    name = 'title',
    x = 150,
    y = 43,
    draw_list=[
        UIText(Black, 0, 0, 'Virtual Music', 1, 2)
    ]
)

PracticeButton = UI_Element(
    name = 'practice',
    x=int(resolution[0] / 2 - 100),
    y=int(resolution[1] / 2),
    draw_list=[
        UIRect(PrimaryColor, 0,0, 200, 50, -1),
        # UIRect((0,0,0), 0,0, 160, 45, 1),
        UIText((255,255,255), 25, 35, 'Practice', 1, 2)
    ]
)

SettingsButton = UI_Element(
    name='settings',
    x=int(resolution[0]-210),
    y=int(15),
    draw_list=[
        UIRect(PrimaryColor, 0, 0, 130, 34, 1),
        UIText(PrimaryColor, 2, 28, 'Settings', 1, 2)
    ]
)

HomeButton = UI_Element(
    name='home',
    x=int(50),
    y=int(15),
    draw_list=[
        UIRect(PrimaryColor, 0, 0, 92, 34, -1),
        UIText(White, 2, 28, 'Home', 1, 2)
    ]
)

HomeScene = Scene(
    name = 'home',
    elements=[
        TitleBig,
        PracticeButton,
        SettingsButton
    ]
)

SettingsScene = Scene(
    name = 'settings',
    elements=[
        TitleSmall,
        HomeButton
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
clickedItems = []

    
        
toggle = True
global activeScene 
activeScene= SettingsScene
def mouse_click(event, x, y, flags, param):
    global activeScene
    if event != cv2.EVENT_LBUTTONDOWN:
        return
    # Click practice button with LMB
    clickedItems = activeScene.check_points([(x,y)])
    if clickedItems != []:
        print(clickedItems)
        if 'home' in clickedItems:
            activeScene = HomeScene
            print(activeScene.name)
        if 'settings' in clickedItems:
            activeScene = SettingsScene
            print(activeScene.name)
while True:
    # Create a white image
    img = np.full((resolution[1],resolution[0],3), 255, np.uint8)
    # HomeScene.render(img)
    # if toggle:
    #     print('By Element')
    #     element_scene.render(img)
    # else:
    #     print('By Shape')
    #     shape_scene.render(img)
    
    activeScene.render(img)
    cv2.imshow("Test UI", img)
    print('Check mouse')
    cv2.setMouseCallback("Test UI", mouse_click)
    print('Done mouse')
    if clickedItems != []:
        print(clickedItems)
        if 'home' in clickedItems:
            activeScene = HomeScene
            print(activeScene.name)
        if 'settings' in clickedItems:
            activeScene = SettingsScene
            print(activeScene.name)
    
    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27:
        print('Exiting')
        cv2.destroyAllWindows()
        break
