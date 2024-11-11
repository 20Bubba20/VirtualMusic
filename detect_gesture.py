import os

import mediapipe as mp
import cv2

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


# Create a image segmenter instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    # cv2.imshow('Show', output_image.numpy_view())
    # imright = output_image.numpy_view()
    # print(result.gestures)
    gesture_list = []
    for id, gesture in enumerate(result.gestures):
        for id_2, gest in enumerate(gesture):
            # print(f'{id} - {id_2}: {type(gest)}, {gest}')
            # print(gest.category_name)
            gesture = (timestamp_ms, id, id_2, gest.category_name, gest.score)
            gesture_list.append(gesture)
            
    return gesture_list
        
    # cv2.imwrite('somefile.jpg', imright)
    
def read_gesture(frame, recognizer, timestamp: int):
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    # Send live image data to perform gesture recognition
    # The results are accessible via the `result_callback` provided in
    # the `GestureRecognizerOptions` object.
    # The gesture recognizer must be created with the live stream mode.
    gesture_list = recognizer.recognize_async(mp_image, timestamp)
    return gesture_list

options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)

def main():
    video = cv2.VideoCapture(0)
    

    timestamp = 0
    with GestureRecognizer.create_from_options(options) as recognizer:
    # The recognizer is initialized. Use it here.
        while video.isOpened(): 
            # Capture frame-by-frame
            ret, frame = video.read()
            if not ret:
                print("Ignoring empty frame")
                continue
            timestamp += 1
            gesture_list = read_gesture(frame, recognizer, timestamp)
            if gesture_list is not None:
                print(gesture_list)
            # print(timestamp)
            cv2.imshow('Show', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    video.release()
    cv2.destroyAllWindows()
    
    
if __name__ == '__main__':
    main()