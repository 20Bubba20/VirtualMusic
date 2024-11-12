import cv2
import mediapipe as mp

from camera_selection import select_camera_cli
from detect_gesture import read_gesture, print_result
from detect_hands import get_points_theremin, detect_hands, draw_hands

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def main():
    camera = select_camera_cli()
    print(f'You have selected {camera.name}')
    
    print('Generate capture')
    capture = cv2.VideoCapture(camera.index, camera.backend)
    print('Capture Generated')
    
    
    timestamp = 0
    state = 'hand'
    resolution = (1000, 1000)
    
    
    print("Initialize gesture detection.")
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=open('gesture_recognizer.task', "rb").read()),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)
    with GestureRecognizer.create_from_options(options) as recognizer:
        print("Gesture detection initialized.")
        while capture.isOpened():
            ret, frame = capture.read()
            if not ret:
                print("Ignoring empty frame")
                continue
            match state:
                case 'hand':
                    hands = detect_hands(frame, resolution)
                    if hands is not None:
                        theremin_points = get_points_theremin(hands)
                    output_image = draw_hands(frame, hands)
                    cv2.imshow("Hand tracker", output_image)
                    # Anything that sets the state to gesture detection (temporarily, it is every 20 cycles)
                    if timestamp % 20 == 0:
                        print("Switching to gesture detection.")
                        state = 'gesture'
                    pass
                case 'gesture':
                    gesture_list = read_gesture(frame, recognizer, timestamp)
                    print(gesture_list)
                    print("Switching to hand detection.")
                    state = 'hand'
                    pass
                case _:
                    state = 'hand'
            timestamp += 1
            if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27:
                print('Exiting')
                break
    
    capture.release()
    cv2.destroyAllWindows()
    pass

if __name__ == '__main__':
    main()