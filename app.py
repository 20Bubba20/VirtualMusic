# Sound Libraries
import time

import imutils
import pyaudio
import numpy as np

# Computer vision libraries
import cv2
import mediapipe as mp

# Custom functions and objects
from camera_selection import select_camera_cli
from detect_gesture import read_gesture, print_result
from detect_hands import get_points_center, detect_hands, draw_hands
from ui_file import *

# Import computer vision object types
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

title = 'Virtual Music'
aspect_ratio = (16, 9)
scale = 80
resolution = (scale * aspect_ratio[0], scale * aspect_ratio[1])  # (1280, 720)
blank_background = np.full((resolution[1], resolution[0], 3), 255, np.uint8)
bufferTime = 5

activeScene = HomeScene
capture = None
timestamp = 0


# Sound sample
def generateSample(frequency, fs, duration):
    return (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)

def mouse_click(event, x, y, flags, param):
    global activeScene, capture
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = activeScene.check_points([(x, y)])
        for hovered in clicked:
            if 'home' in hovered:
                print("Changing Scene")
                activeScene = HomeScene
                activeScene.scene_start = timestamp
                break
            elif 'settings' in hovered:
                print("Changing Scene")
                activeScene = SettingsScene
                activeScene.scene_start = timestamp
                break
            elif 'practice' in hovered:
                print("Changing Scene")
                activeScene = ThereminPractice
                activeScene.scene_start = timestamp
                break
            elif 'camera-' in hovered:
                camera_object = hovered
                print(camera_object)
                camera = camera_object.split('-')[1]
                index = camera.split(',')[0]
                backend = camera.split(',')[1]
                print(index, backend)
                capture.release()
                capture = cv2.VideoCapture(int(index), int(backend))
                activeScene.scene_start = timestamp
                break
            elif 'exit' in hovered:
                print("Exiting")
                capture.release()
                cv2.destroyAllWindows()

# Home Scene
def home(recognizer, timestamp) -> Scene:
    global activeScene, capture
    background = np.full((resolution[1], resolution[0], 3), 255, np.uint8)
    _, img = capture.read()
    img = cv2.flip(img, 1)
    
    hands = None
    try:
        hands = detect_hands(img, resolution)
    except Exception as err:
        #print(err)
        pass
    
    activeScene.render(background)

    # Determine where the hands are & what gestures
    # Check if there is a hand
    if hands is not None:
        home_points = get_points_center(hands)
        hovered_objects = []
        # Draw a spot for each hand
        for hand in home_points:
            cv2.circle(background, hand, 10, Red, cv2.FILLED)
        
        # Ensuring no accidental selections by waiting a buffer
        if timestamp - activeScene.scene_start > bufferTime:
            
            # Check if the hand is in an area
            hovered_objects = activeScene.check_points(home_points)

        # Event Handler
        # def mouse_click(event, x, y, flags, param):
        #     global activeScene
        #     if event == cv2.EVENT_LBUTTONDOWN:
        #         clicked = activeScene.check_points([(x, y)])
        #         for hovered in clicked:
        #             if 'settings' in hovered:
        #                 print("Changing Scene")
        #                 activeScene = SettingsScene
        #                 activeScene.scene_start = timestamp
        #                 break
        #             if 'practice' in hovered:
        #                 print("Changing Scene")
        #                 activeScene = ThereminPractice
        #                 activeScene.scene_start = timestamp
        #                 break

        # try:
        #     cv2.setMouseCallback(title, mouse_click)
        # except:
        #     pass
        
        if hovered_objects != []:
            # Get Gesture(s)
            gesture_list = read_gesture(img, recognizer, timestamp)
            gestures = []
            for gesture in gesture_list:
                print(gesture)
                # For testing to make sure index is correct
                for index, value in enumerate(gesture):
                    print(index, value)
                gestures.append(gesture[3])
            print(gestures)

        

            # Is the hand in an area? If so, is it a Closed_Fist?

            if 'Closed_Fist' in gestures:
                for hovered in hovered_objects:
                    if 'settings' in hovered:
                        print("Changing Scene")
                        activeScene = SettingsScene
                        activeScene.scene_start = timestamp
                        break
                    if 'practice' in hovered:
                        print("Changing Scene")
                        activeScene = ThereminPractice
                        activeScene.scene_start = timestamp
                        break
                    if 'exit' in hovered:
                        print("Exiting")
                        capture.release()
                        cv2.destroyAllWindows()
        pass
    cv2.imshow(title, background)
    # return activeScene


# Settings Scene
def settings(recognizer, timestamp) -> tuple:
    global activeScene, capture
    ret, img = capture.read()
    # print(capture.getBackendName(), ret, img is None)
    img = cv2.flip(img, 1)
    background = np.full((resolution[1], resolution[0], 3), 255, np.uint8)
    hands = None
    try:
        hands = detect_hands(img, resolution)
    except Exception as err:
        #print(err)
        pass
    # time_entered = -1

    activeScene.render(background)

    # Determine where the hands are & what gestures
    # Check if there is a hand
    if hands is not None:
        home_points = get_points_center(hands)
        hovered_objects = []
        # Draw a spot for each hand
        for hand in home_points:
            cv2.circle(background, hand, 10, Red, cv2.FILLED)
        
        # Ensuring no accidental selections by waiting a buffer
        if timestamp - activeScene.scene_start > bufferTime:
            
            # Check if the hand is in an area
            hovered_objects = activeScene.check_points(home_points)
        
        # Event Handler
        # def mouse_click(event, x, y, flags, param):
        #     global activeScene, capture
        #     if event == cv2.EVENT_LBUTTONDOWN:
        #         clicked = activeScene.check_points([(x, y)])
        #         for hovered in clicked:
        #             if 'camera-' in hovered:
        #                 camera_object = hovered
        #                 print(camera_object)
        #                 camera = camera_object.split('-')[1]
        #                 index = camera.split(',')[0]
        #                 backend = camera.split(',')[1]
        #                 print(index, backend)
        #                 capture.release()
        #                 capture = cv2.VideoCapture(int(index), int(backend))
        #                 activeScene.scene_start = timestamp
        #                 break
        #             if 'settings' in hovered:
        #                 print("Changing Scene")
        #                 activeScene = SettingsScene
        #                 activeScene.scene_start = timestamp
        #                 break
        #             if 'home' in hovered:
        #                 print("Changing Scene")
        #                 activeScene = HomeScene
        #                 activeScene.scene_start = timestamp
        #                 break
        #             if 'exit' in hovered:
        #                 print("Exiting")
        #                 capture.release()
        #                 cv2.destroyAllWindows()

        # try:
        #     cv2.setMouseCallback(title, mouse_click)
        # except:
        #     pass
        
        if hovered_objects != []:
            # Get Gesture(s)
            gesture_list = read_gesture(img, recognizer, timestamp)
            gestures = []
            for gesture in gesture_list:
                print(gesture)
                # For testing to make sure index is correct
                for index, value in enumerate(gesture):
                    print(index, value)
                gestures.append(gesture[3])
            print(gestures)
            camera_object = None
            if 'Closed_Fist' in gestures:
                for hovered in hovered_objects:
                    if 'camera-' in hovered:
                        camera_object = hovered
                        print(camera_object)
                        camera = camera_object.split('-')[1]
                        index = camera.split(',')[0]
                        backend = camera.split(',')[1]
                        print(index, backend)
                        capture.release()
                        capture = cv2.VideoCapture(int(index), int(backend))
                        activeScene.scene_start = timestamp
                        break
                    if 'home' in hovered:
                        print("Changing Scene")
                        activeScene = HomeScene
                        activeScene.scene_start = timestamp
                        break
                    if 'exit' in hovered:
                        print("Exiting")
                        capture.release()
                        cv2.destroyAllWindows()
                        # return activeScene, capture
    cv2.imshow(title, background)
    # return activeScene, capture

# Theremin Practice Scene
def theremin(recognizer, timestamp, stream) -> Scene:
    global activeScene, capture
    _, img = capture.read()
    img = cv2.flip(img, 1)
    img = imutils.resize(img, width=resolution[0], height=resolution[1])
    fs = 44100  # sampling rate, Hz, must be integer
    duration = 0.1  # in seconds, may be a float
    
    hands = None
    try:
        hands = detect_hands(img, resolution)
    except Exception as err:
        #print(err)
        pass
    
    activeScene.render(img)

    # Determine where the hands are & what gestures
    # Check if there is a hand
    if hands is not None:
        theremin_points = get_points_center(hands)
        hovered_objects = []
        # Draw a spot for each hand
        for hand in theremin_points:
            cv2.circle(img, hand, 10, Red, cv2.FILLED)
        
        # Ensuring no accidental selections by waiting a buffer
        if timestamp - activeScene.scene_start > bufferTime:
            
            # Check if the hand is in an area
            hovered_objects = activeScene.check_points(theremin_points)

        # Event Handler
        # def mouse_click(event, x, y, flags, param):
        #     global activeScene
        #     if event == cv2.EVENT_LBUTTONDOWN:
        #         clicked = activeScene.check_points([(x, y)])
            
        #         for hovered in clicked:
        #             if 'settings' in hovered:
        #                 print("Changing Scene")
        #                 activeScene = SettingsScene
        #                 activeScene.scene_start = timestamp
        #                 break
        #             if 'home' in hovered:
        #                 print("Changing Scene")
        #                 activeScene = HomeScene
        #                 activeScene.scene_start = timestamp
        #                 break
        # try:
        #     cv2.setMouseCallback(title, mouse_click)
        # except:
        #     pass
        
        if hovered_objects != []:
            # Get Gesture(s)
            gesture_list = read_gesture(img, recognizer, timestamp)
            gestures = []
            for gesture in gesture_list:
                print(gesture)
                # For testing to make sure index is correct
                for index, value in enumerate(gesture):
                    print(index, value)
                gestures.append(gesture[3])
            print(gestures)


            # Is the hand in an area? If so, is it a Closed_Fist?

            if 'Closed_Fist' in gestures:
                for hovered in hovered_objects:
                    if 'settings' in hovered:
                        print("Changing Scene")
                        activeScene = SettingsScene
                        activeScene.scene_start = timestamp
                        break
                    if 'home' in hovered:
                        print("Changing Scene")
                        activeScene = HomeScene
                        activeScene.scene_start = timestamp
                        break
            for hovered in hovered_objects:    
                if 'theremin' in hovered:
                    # Play Tone
                    x, y = theremin_points[0]
                    # x -> frequency
                    frequency = np.interp(x, [0, resolution[0]], [130.81, 193.88])
                    # y -> volume
                    volume = np.interp(y, [0, resolution[1]], [0.10, 0.80])

                    samples = generateSample(frequency, fs, duration)
                    stream.write(volume * samples)
                    break
        pass
    cv2.imshow(title, img)
    # return activeScene


# Creates a countdown confirmation when selecting buttons with your hand
def countdownLoader(newScene: Scene, timestamp, time_entered):
    if time_entered == -1:
        return timestamp
    else:
        time_diff = timestamp - time_entered

        # Text on the UI of how long until selection
        counting = UIText(Black, 0, 0, str(time_diff), 2, 4)

        if time_diff > bufferTime:
            activeScene = newScene
            activeScene.scene_start = timestamp
            return -1


def main():
    global activeScene, capture, timestamp
    if len(SettingsScene.contents) < 6:
        SettingsScene.contents.extend(generateCameraSelect())
    
    activeScene = HomeScene
    activeScene.scene_start = 0
    camera = 0
    while True:
        capture = cv2.VideoCapture(camera)
        ret, _ = capture.read()
        if ret:
            break
        camera = camera + 1

    timestamp = 0
    state = 'hand'

    # Initialize Audio
    p = pyaudio.PyAudio()
    # Parameters
    fs = 44100  # sampling rate, Hz, must be integer
    # Open stream
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    print("Initialize gesture detection.")
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=open('gesture_recognizer.task', "rb").read()),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)
    with GestureRecognizer.create_from_options(options) as recognizer:
        print("Gesture detection initialized.")

        # Setting what each scene needs when hands are captured
        while capture.isOpened():
            if activeScene.name == 'practice-theremin':
                theremin(recognizer, timestamp, stream)

            if activeScene.name == 'home':
                home(recognizer, timestamp)

            if activeScene.name == 'settings':
                settings(recognizer, timestamp)

            # Increment time
            timestamp += 1

            # Exit
            if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27:
                print('Exiting')
                break
            try:
                cv2.setMouseCallback(title, mouse_click)
            except:
                passq
            
            

    capture.release()
    cv2.destroyAllWindows()
    # stream.close()

    p.terminate()
    pass


if __name__ == '__main__':
    main()
