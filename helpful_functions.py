import cv2

def check_camera(camera: int, cap: cv2.VideoCapture, next_key: str| int = 'n', previous_key: str| int = 'p') -> tuple[int, cv2.VideoCapture]:
    """Check user input if they want to change the camera

    Args:
        camera (int): ID to identify the camera
        cap (cv2.VideoCapture): CV2 video capture object that is used to get the data from the camera
        next_key (str| int, optional): Letter of key or unicode value of the key that is used to change the camera. Default is 'n'
        previous_key (str| int, optional): Letter of key or unicode value of the key that is used to change the camera. Default is 'p'

    Raises:
        Exception: camera does not exist, looped back to camera 0

    Returns:
        tuple[int, cv2.VideoCapture]: The new values for the entered camera id and video capure object
    """
    
    if change_key is str:
        change_key = ord(change_key)
    
    key = cv2.waitKey(1)
    if key == next_key:
        camera += 1
        pass
    elif key == previous_key:
        camera -= 1
        pass
    else: # No Change
        return camera, cap
        
    try:
        cap = cv2.VideoCapture(camera)
        # Detect if the new camera works
        if cap.read()[1] is None:
            raise Exception()
    except:
        # Reset to default if failed
        camera = 0
        cap = cv2.VideoCapture(camera)
    print(f'Camera {camera}')
    print('Go to NEXT camere using "n" or EXIT using ESC or "q"')
            
    return camera, cap

def function(variable: int = 1):
    """_summary_

    Args:
        variable (int, optional): _description_. Defaults to 1.
    """
    pass