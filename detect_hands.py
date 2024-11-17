import cv2
import mediapipe as mp
import imutils
from helpful_functions import check_camera

# Global Variables
# - Media Pipe setup
# print("Setting Global variables")
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
# print("Done: Setting Global variables")


def detect_hands(image, resolution: tuple[int, int]) -> list:
    """Take image generated from Video Capture and get the 21 reference points and the center point

    Args:
        image (Matlike | Any): image taken from Video Capture
        resolution (tuple): A two tuple that contains the desired hight and width of the image (width, height)
    
    Returns:
        list[tuple]: List containing up to two hands, each represented by a three-tuple:
            * the x,y coordinates of the center of the hand
            * a list of the 21 reference points for the hand
            * CV2 object representing the hand - only used for testing purposes
    """
    
    try:
        image = imutils.resize(image, width=resolution[0], height=resolution[1])
    except:
        raise Exception ("Detect Hands Failed - Image Resizing")
    
    # Converting the input to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(gray_image)
    
    # Check if there are hands
    if not results.multi_hand_landmarks:
        return None
    
    # List of hands in frame (testing showed max of 2)
    
    hand_positions = []
    for i in range(len(results.multi_hand_landmarks)):
        hand_lms = results.multi_hand_landmarks[i]
        handpoints = []
        sum_x = 0
        sum_y = 0
        for id, lm in enumerate(hand_lms.landmark):
            h, w, c = image.shape

            # Finding the coordinates of each landmark
            cx, cy = int(lm.x * w), int(lm.y * h)
            sum_x += cx
            sum_y += cy

            # Printing each landmark ID and coordinates
            # on the terminal
            handpoints.append((id, cx, cy))

        # Calculate hand position by averageing all of the hand points
        
        hand_pos = (int((sum_x/len(handpoints))*w), int((sum_y/len(handpoints))*h))
        
        
        hand_positions.append((hand_pos, handpoints, hand_lms))
        # print('Hand Position:', hand_pos)
    
    return hand_positions

def get_points_theremin(hand_positions: list[tuple[tuple, list[tuple[int, int]], list]]) -> list[tuple[int, int]]:
    """Take a list of hand positions and return only the ones needed for the theremin

    Args:
        hand_positions (list[tuple[tuple, list[tuple[int, int]], list]]): List containing all of the hand information

    Returns:
        list[tuple[int, int]]: list of points to be used in the processing for the theremin
    """
    
    hand_points = []
    if hand_positions is not None:
        for hand in hand_positions:
            hand_points.append(hand[0])
    return hand_points

def get_points_piano(hand_positions: list[tuple[tuple, list[tuple[int, int]], list]]) -> list[tuple[int, int]]:
    """Take a list of hand positions and return only the ones needed for the piano

    Args:
        hand_positions (list[tuple[tuple, list[tuple[int, int]], list]]): List containing all of the hand information

    Returns:
        list[tuple[int, int]]: list of points to be used in the processing for the piano
    """
    # Points given by https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
    required_points = [4, 8, 12, 16, 20]
    hand_points: list[tuple[int,int]] = []
    if hand_positions is not None:
        for hand in hand_positions:
            center = hand[0]
            hand_points.append(center)
            finger_tips = []
            for id, point in enumerate(hand[1]):
                if id not in required_points:
                    continue
                finger_tips.append(point)
            hand_points.extend(finger_tips)
    return hand_points

def get_points_guitar(hand_positions: list[tuple[tuple, list[tuple[int, int]], list]]) -> list[tuple[int, int]]:
    """Take a list of hand positions and return only the ones needed for the guitar

    Args:
        hand_positions (list[tuple[tuple, list[tuple[int, int]], list]]): List containing all of the hand information

    Returns:
        list[tuple[int, int]]: list of points to be used in the processing for the guitar
    """
    # Points given by https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
    required_points = [4, 8, 12, 16, 20]
    hand_points: list[tuple[int,int]] = []
    if hand_positions is not None:
        for hand in hand_positions:
            finger_tips = []
            for id, point in enumerate(hand[1]):
                if id not in required_points:
                    continue
                finger_tips.append(point)
            hand_points.extend(finger_tips)
    return hand_points

def draw_hands(img, hand_positions: list[tuple]):
    """Draw the hands on the source image

    Args:
        img (Matlike | Any): image taken from Video Capture
        hand_positions (list[tuple]): list: List containing up to two hands, each represented by a three-tuple

    Returns:
        Matlike | Any: Resulting image from the draw
    """
    color_dict = [
        (86, 41, 79),
        (99, 46, 84),
        (113, 52, 88),
        (126, 58, 92),
        (140, 64, 94),
        (152, 71, 97),
        (165, 79, 98),
        (177, 87, 99),
        (188, 95, 100),
        (199, 105, 100),
        (209, 115, 100),
        (218, 126, 99),
        (226, 137, 99),
        (232, 149, 99),
        (238, 161, 99),
        (243, 174, 100),
        (247, 187, 101),
        (249, 200, 103),
        (250, 214, 107),
        (250, 228, 112),
        (250, 230, 119)
    ]
    if hand_positions is None:
        return img
    
    for hand in hand_positions:
        h, w, c = img.shape
        hand_pos = hand[0]
        hand_points = hand[1]
        hand_lms = hand[2]
        
        for id, point in enumerate(hand_points):
            

            # Finding the coordinates of each landmark
            cx, cy = int(point[0] * w), int(point[1] * h)

            # Creating a circle around each landmark
            cv2.circle(img, (cx, cy), 10, color_dict[id],
                        cv2.FILLED)
            # Drawing the landmark connections
            mpDraw.draw_landmarks(img, hand_lms,
                                    mpHands.HAND_CONNECTIONS)
        cv2.circle(img, hand_pos, 10, (125,125,125),
                       cv2.FILLED)
    return img


    pass
def main():
    """
    For Testing purposes only
    """
    # Set default camera 0 and prefered resolution of 1000px x 1000px
    camera = 0
    resolution = (1000,1000)
    print(f'Camera {camera}')
    cap = cv2.VideoCapture(camera)
    while True:
        success, image = cap.read()
    
        hand_positions = detect_hands(image, resolution)
        
        
        if hand_positions is not None:
            for i in range(len(hand_positions)):
                if hand_positions[i] is None:
                    continue
                print(f'Points for hand {i}: {len(hand_positions[i][1])}')
                # print(hand_positions[i])
            
            # Draw the hands
            image = draw_hands(image, hand_positions)
            
        # Display the output
        cv2.imshow("Hand tracker", image)        
        
        # Check for camera change
        camera, cap = check_camera(camera, cap)
        
        # Program terminates when q key or ESC key is pressed
        if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27:
            print('Exiting')
            cap.release()
            cv2.destroyAllWindows()
            break
    
if __name__=="__main__":
    main()