# Sound Libraries
import pyaudio
import numpy as np

# Computer vision libraries
import cv2
import mediapipe as mp

# Custiom functions and objects
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

# Sound sample
def generateSample(frequency, fs, duration):
    return (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)

# Home Scene
def home(activeScene: Scene, capture, recognizer, timestamp) -> Scene:
    background = np.full((resolution[1], resolution[0], 3), 255, np.uint8)
    ret, img = capture.read()
    img = cv2.flip(img, 1)
    hands = detect_hands(img, resolution)
    activeScene.render(background)

    # Determine where the hands are & what gestures
    # Check if there is a hand
    if hands is not None:
        home_points = get_points_center(hands)
        hovered_objects = activeScene.check_points(home_points)

        # Event Handler
        def mouse_click(event, x, y, flags, param):
            hovered_objects.extend(activeScene.check_points([(x, y)]))
        cv2.setMouseCallback(title, mouse_click)

        # Is the hand in an area? If so, is it a Closed_Fist?
        for hand in home_points:
            print(hand)
            cv2.circle(background, (resolution[0] - hand[0], hand[1]), 10, PrimaryColor, cv2.FILLED)
            pass

        # Ensuring no accidental selections by waiting a buffer
        # Practice button
        if timestamp - activeScene.scene_start > bufferTime and 'practice' in hovered_objects:
            gesture_list = read_gesture(img, recognizer, timestamp)
            if 'Closed_Fist' in gesture_list:
                activeScene = ThereminPractice
                activeScene.scene_start = timestamp

        # Settings button
        elif timestamp - activeScene.scene_start > bufferTime and 'settings' in hovered_objects:
            gesture_list = read_gesture(img, recognizer, timestamp)
            if 'Closed_Fist' in gesture_list:
                activeScene = SettingsScene
                activeScene.scene_start = timestamp

        pass
    cv2.imshow(title, background)
    return activeScene


# Settings Scene
def settings(activeScene: Scene, capture, recognizer, timestamp) -> tuple:
    ret, img = capture.read()
    img = cv2.flip(img, 1)
    background = np.full((resolution[1], resolution[0], 3), 255, np.uint8)
    hands = detect_hands(img, resolution)

    if len(activeScene.contents) < 5:
        activeScene.contents.extend(generateCameraSelect())
    activeScene.render(background)

    # Determine where the hands are & what gestures
    # Check if there is a hand
    if hands is not None:
        home_points = get_points_center(hands)
        hovered_objects = activeScene.check_points(home_points)

        # Is the hand in an area? If so, is it a Closed_Fist?
        for hand in home_points:
            cv2.circle(background, hand, 10, PrimaryColor, cv2.FILLED)
        print(hovered_objects)

        # Ensuring no accidental selections by waiting a buffer
        # Home button
        if timestamp - activeScene.scene_start > bufferTime and 'home' in hovered_objects:
            gesture_list = read_gesture(img, recognizer, timestamp)
            print(gesture_list)
            gestures = []
            for gesture in gesture_list:
                gestures.append(gesture[3])
            if 'Closed_Fist' in gestures:
                activeScene = HomeScene
                activeScene.scene_start = timestamp

        # Exit button
        elif timestamp - activeScene.scene_start > bufferTime and 'exit' in hovered_objects:
            gesture_list = read_gesture(img, recognizer, timestamp)
            print(gesture_list)
            gestures = []
            for gesture in gesture_list:
                gestures.append(gesture[3])
            if 'Closed_Fist' in gestures:
                cv2.imshow(title, background)
                capture.release()
                cv2.destroyAllWindows()
                return activeScene

        # Camera selection
        elif timestamp - activeScene.scene_start > bufferTime:
            camera_object = None
            for hovered in hovered_objects:
                if 'camera-' in hovered:
                    camera_object = hovered
                    break
            if camera_object is not None:
                gesture_list = read_gesture(img, recognizer, timestamp)
                print(gesture_list)
                gestures = []
                for gesture in gesture_list:
                    gestures.append(gesture[3])
                if 'Closed_Fist' in gestures:
                    print(camera_object)
                    camera = camera_object.split('-')[1]
                    index = camera.split(',')[0]
                    backend = camera.split(',')[1]
                    print(index, backend)
                    capture = cv2.VideoCapture(int(index), int(backend))
                    activeScene.scene_start = timestamp

            pass
        pass
    cv2.imshow(title, background)
    return activeScene, capture


# Theremin Practice Scene
def theremin(activeScene: Scene, capture, recognizer, timestamp, stream) -> Scene:
    ret, img = capture.read()
    img = cv2.flip(img, 1)
    hands = detect_hands(img, resolution)
    fs = 44100  # sampling rate, Hz, must be integer
    duration = 0.1  # in seconds, may be float
    activeScene.render(img)

    # Determine where the hands are & what gestures
    # Check if there is a hand
    if hands is not None:
        theremin_points = get_points_center(hands)

        hand_pos = theremin_points[0]
        hovered_objects = activeScene.check_points([hand_pos])

        # If the theremin is not being played
        if 'theremin' not in hovered_objects:

            # Ensuring no accidental selections by waiting a buffer
            # Home button
            if timestamp - activeScene.scene_start > bufferTime and 'home' in hovered_objects:
                gesture_list = read_gesture(img, recognizer, timestamp)
                if 'Closed_Fist' in gesture_list:
                    activeScene = HomeScene
                    activeScene.scene_start = timestamp

            # Settings button
            elif timestamp - activeScene.scene_start > bufferTime and 'settings' in hovered_objects:
                gesture_list = read_gesture(img, recognizer, timestamp)
                if 'Closed_Fist' in gesture_list:
                    activeScene = SettingsScene
                    activeScene.scene_start = timestamp

        else:
            # Play Tone
            x, y = theremin_points[0]
            # x -> frequency
            frequency = np.interp(x, [0, resolution[0]], [130.81, 193.88])
            # y -> volume
            volume = np.interp(y, [0, resolution[1]], [0.10, 0.80])

            samples = generateSample(frequency, fs, duration)
            stream.write(volume * samples)
            cv2.circle(img, hand_pos, 10, PrimaryColor, cv2.FILLED)
    cv2.imshow(title, img)
    return activeScene


def main():
    activeScene = SettingsScene
    capture = cv2.VideoCapture(0)

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

        while capture.isOpened():

            if activeScene.name == 'practice-theremin':
                activeScene = theremin(activeScene, capture, recognizer, timestamp, stream)

            if activeScene.name == 'home':
                activeScene = home(activeScene, capture, recognizer, timestamp)

            if activeScene.name == 'settings':
                activeScene, capture = settings(activeScene, capture, recognizer, timestamp)
            timestamp += 1
            if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27:
                print('Exiting')
                break

    capture.release()
    cv2.destroyAllWindows()
    # stream.close()

    p.terminate()
    pass


if __name__ == '__main__':
    main()
