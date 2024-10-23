import cv2

def check_camera(camera: int, cap) -> int:
    # Use the n key to switch cameras
    if cv2.waitKey(1) == ord('n'):
        camera += 1
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