import numpy as np
import cv2
from ui_objects import *
from cv2_enumerate_cameras import enumerate_cameras

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

Cameras = UI_Element(
    name = 'cameras',
    x = int(resolution[0] / 2 - 200),
    y = 200,
    draw_list=[
        UIText((0, 0, 0), 0, 0, 'Select Camera', 2, 4)
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

ExitInstruct = UI_Element(
    name='exit',
    x=int(resolution[0] / 2 - 300),
    y=int(resolution[1] - 50),
    draw_list=[
        UIText(Black, 0, 0, 'Press "Escape" or the "Q" key to exit.', 1, 2)
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

ExitButton = UI_Element(
    name='exit',
    x=int(resolution[0]-210),
    y=int(15),
    draw_list=[
        UIRect(PrimaryColor, 0, 0, 130, 34, 1),
        UIText(PrimaryColor, 2, 28, 'Exit', 1, 2)
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

ThereminSpace = UI_Element(
    name='theremin',
    x = 150,
    y = 100,
    draw_list=[
        UIRect(Black, 0, 0, int(resolution[0]-200), int(resolution[1]-200), 4)
    ]
)

HomeScene = Scene(
    name = 'home',
    elements=[
        TitleBig,
        PracticeButton,
        SettingsButton,
        ExitInstruct
    ]
)

SettingsScene = Scene(
    name = 'settings',
    elements=[
        TitleSmall,
        Cameras,
        HomeButton,
        ExitButton
    ]
)

ThereminPractice = Scene(
    name='practice-theremin',
    elements=[
        TitleSmall,
        HomeButton,
        SettingsButton,
        ThereminSpace
    ]
)

def generateCameraSelect():
    available_cameras = enumerate_cameras()

    listStart = (int(resolution[0] / 2 - 200), 250)
    if not available_cameras:
        NoCameras = UI_Element(
            name = 'no_camera',
            x = listStart[0],
            y = listStart[1],
            draw_list=[
                UIRect(PrimaryColor, 0, 0, 150, 34, -1),
                UIText(White, 2, 28, 'No Cameras', 1, 2)
            ]
        )
        return [NoCameras]
   


    print("Available cameras:")
    offset = 0
    camera_list = []
    for id, camera_info in enumerate(available_cameras):
        print(f'{id}: {camera_info.name}')
        try:
            capture = cv2.VideoCapture(camera_info.index, camera_info.backend)
            ret, img = capture.read()
            if not ret:
                raise Exception()
        except:
            continue
        cameraButton = UI_Element(
            name = f'camera-{camera_info.index},{camera_info.backend}',
            x = listStart[0],
            y = listStart[1] + offset,
            draw_list=[
                UIRect(PrimaryColor, 0, 0, 150, 50, -1),
                UIText(White, 2, 28, camera_info.name, 1, 2)
            ]
        )
        camera_list.append(cameraButton)
        offset = offset + 60
    return camera_list
    pass