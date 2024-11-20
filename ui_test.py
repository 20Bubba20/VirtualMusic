import numpy as np
import cv2
from ui_objects import *

scale = (16, 9)
k = 80
resolution = (k*scale[0],k*scale[1])
# print(resolution)
PrimaryColor = (18, 96, 132)
TitleBig = UI_Element(
    name = 'title',
    x = int((resolution[0]/2)),
    y = 120,
    draw_list=[
        UIText((0, 0, 0), 0, 0, 'Virtual Music', 2, 4),
        UIEllipse((0,0,0), 0,0, 3, 3, -1)
    ]
)

PracticeButton = UI_Element(
    name = 'practice',
    x = int((resolution[0]/2))-50,
    y = 155,
    draw_list=[
        UIRect(PrimaryColor, 0,0, 300, 20, -1),
        UIRect((0,0,0), 0,0, 300, 20, -1),
        UIText((255,255,255), 15, 15, 'Practice', 1, 2)
    ]
)


HomeScene = [
    TitleBig
]


while True:
    # Create a white image
    img = np.full((resolution[1],resolution[0],3), 255, np.uint8)
    for element in HomeScene:
        element.draw(img)
    cv2.imshow("Test UI", img)
    
    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27:
        print('Exiting')
        cv2.destroyAllWindows()
        break
