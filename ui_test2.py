import numpy as np
import cv2
from ui_objects import *

scale = (16, 9)
k = 80
resolution = (k * scale[0], k * scale[1])  # (1280, 720)
# print(resolution)

PrimaryColor = (132, 96, 18)
White = (255, 255, 255)
Black = (0, 0, 0)

TitleBig = UI_Element(
    name='title',
    x=int(resolution[0] / 2 - 200),
    y=200,
    draw_list=[
        UIText(Black, 0, 0, 'Virtual Music', 2, 4),
    ]
)

PracticeButton = UI_Element(
    name='practice',
    x=int(resolution[0] / 2 - 100),
    y=int(resolution[1] / 2),
    draw_list=[
        UIRect(PrimaryColor, 0, 0, 200, 50, -1),
        # UIRect((0,0,0), 0,0, 160, 45, 1),
        UIText(White, 25, 35, 'Practice', 1, 2)
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

def mouse_click(event, x, y, flags, param):
    global is_exit_clicked
    # Click practice button with LMB
    if PracticeButton.check_within(x, y) and event == cv2.EVENT_LBUTTONDOWN:
        print("Practice button clicked")

HomeScene = Scene(
    name='home',
    elements=[
        TitleBig,
        PracticeButton,
        ExitInstruct
    ]
)

toggle = True

while True:
    # Create a white image
    img = np.full((resolution[1], resolution[0], 3), 255, np.uint8)
    # HomeScene.render(img)

    HomeScene.render(img)
    cv2.imshow("Test UI", img)

    cv2.setMouseCallback("Test UI", mouse_click)

    if cv2.waitKey(-1) == ord('q') or cv2.waitKey(-1) == 27:
        print('Exiting')
        cv2.destroyAllWindows()
        break # Stops loop if 'Q' or `Escape` keys are pressed

    print('Switching')
    toggle = not toggle


