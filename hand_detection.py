import cv2
import mediapipe as mp
import imutils

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

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
def process_image(img):
    # Converting the input to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(gray_image)

    # Returning the detected hands to calling function
    return results

# Drawing landmark connections
def draw_hand_connections(img, results):
    if results.multi_hand_landmarks:
        points = []
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
                
            sum_x = 0
            sum_y = 0
            for id, x, y in handpoints:
                sum_x += x
                sum_y += y
            hand_pos = (int(sum_x/len(handpoints)), int(sum_y/len(handpoints)))
            cv2.circle(img, hand_pos, 10, (125,125,125),
                           cv2.FILLED)
            points.extend(handpoints)
            hand_positions.append((hand_pos,handpoints))
            # print('Hand Position:', hand_pos)
        return img, hand_positions
    return None, None

def main():
    # Replace 0 with the video path to use a
    # pre-recorded video
    camera = 0
    selected = False
    resolution = (1000,1000)
    print(f'Camera {camera}')
    cap = cv2.VideoCapture(camera)
    print('Selecting camera: Hit "n" for NEXT or "y" for YES')
    hand_que = []
    while True:
        # Taking the input
        success, image = cap.read()
        try:
            image = imutils.resize(image, width=resolution[0], height=resolution[0])
        except:
            print(f'Camera {camera} Failed')
            break
        results = process_image(image)
        img, hand_positions = draw_hand_connections(image, results)
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


        if cv2.waitKey(1) == ord('n'):
            camera += 1
            try:
                cap = cv2.VideoCapture(camera)
                if cap.read()[1] is None:
                    raise Exception()
            except:
                camera = 0
                cap = cv2.VideoCapture(camera)
            print(f'Camera {camera}')
            print('Selecting camera: Hit "n" for NEXT or "q" to EXIT')

        # Program terminates when q key is pressed
        if cv2.waitKey(1) == ord('q'):
            print('Exiting')
            cap.release()
            cv2.destroyAllWindows()
            break
    pass
if __name__ == "__main__":
    main()