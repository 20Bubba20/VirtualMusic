import cv2
import mediapipe as mp
import imutils

# Global Variables
# - Media Pipe setup
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# - 21 step Color Gradient
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

# Processing the input image
def get_hands(img):
    # Converting the input to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(gray_image)

    # Returning the detected hands to calling function
    return results

# Drawing landmark connections
def draw_hand_connections(img, results):
    # Check if there are hands
    if not results.multi_hand_landmarks:
        return None, None

    # List of hands in frame (testing showed max of 2)
    # - average position, list of positions
    hand_positions = []
    for i in range(len(results.multi_hand_landmarks)):
        handLms = results.multi_hand_landmarks[i]
        handpoints = []
        for id, lm in enumerate(handLms.landmark):
            h, w, c = img.shape

            # Finding the coordinates of each landmark
            cx, cy = int(lm.x * w), int(lm.y * h)

            # Printing each landmark ID and coordinates
            # on the terminal
            handpoints.append((id, cx, cy))

            # Creating a circle around each landmark
            cv2.circle(img, (cx, cy), 10, color_dict[id],
                       cv2.FILLED)
            # Drawing the landmark connections
            mpDraw.draw_landmarks(img, handLms,
                                  mpHands.HAND_CONNECTIONS)

        # Calculate hand position 
        sum_x = 0
        sum_y = 0
        for id, x, y in handpoints:
            sum_x += x
            sum_y += y
        hand_pos = (int(sum_x/len(handpoints)), int(sum_y/len(handpoints)))
        cv2.circle(img, hand_pos, 10, (125,125,125),
                       cv2.FILLED)
        hand_positions.append((hand_pos,handpoints))
        # print('Hand Position:', hand_pos)
    return img, hand_positions

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
        print('Hit "n" for NEXT or "q" to EXIT')
            
    return camera, cap
    
def main():
    # Set default camera 0 and prefered resolution of 1000px x 1000px
    camera = 0
    resolution = (1000,1000)
    print(f'Camera {camera}')
    print('Hit "n" for NEXT or "q" to EXIT')
    cap = cv2.VideoCapture(camera)

    # Set list of saved hand positions for movement tracking
    hand_que = []
    while True:
        # Taking the input
        success, image = cap.read()
        try:
            image = imutils.resize(image, width=resolution[0], height=resolution[0])
        except:
            print(f'Camera {camera} Failed')
            break

        # Get hand detection results and draw points
        results = get_hands(image)
        img, hand_positions = draw_hand_connections(image, results)

        # Draw the current and previous 25 hand positons
        if hand_positions is not None:
            if len(hand_que) > len(hand_positions):
                hand_que = []
                pass
            if len(hand_que) < len(hand_positions):
                hand_que.extend([[None]]*(len(hand_positions)-len(hand_que)))
                # print(len(hand_positions))
                # print(len(hand_que))
                pass
            for i in range(len(hand_positions)):
                if len(hand_que[i]) <= len(hand_positions[i]):
                    hand_que[i].extend([]*(len(hand_positions[i])-len(hand_que[i])))
                    pass
                hand_que[i].append(hand_positions[i][0])
                if len(hand_que[i]) > 25:
                    hand_que[i].pop(0)
            for i in range(len(hand_que)):
                for j in range(len(hand_que[i])):
                    cv2.circle(image, hand_que[i][j], 10, color_dict[j % 21],
                            cv2.FILLED)
        # Displaying the output
        cv2.imshow("Hand tracker", image)

        camera, cap = check_camera(camera, cap)

        # Program terminates when q key is pressed
        if cv2.waitKey(1) == ord('q'):
            print('Exiting')
            cap.release()
            cv2.destroyAllWindows()
            break
    pass
if __name__ == "__main__":
    main()
