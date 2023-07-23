import cv2
import mediapipe as mp
import pyautogui 
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)


def euclidean_distance(index, thumb):
    return math.sqrt((thumb[0] - index[0])**2 + (thumb[1] - index[1])**2)

def action_handler(image, index, thumb):
    distance = euclidean_distance(thumb, index)

    if distance < 20:
        divide_screen(image, index, thumb)
   
def divide_screen(image, index, thumb):
    height, width = image.shape[:2]

    # Calculate the coordinates to divide the screen into six equal parts
    top = 0
    left = 0
    bottom = height // 2
    right = width // 3

    # Divide the screen into six equal parts
    top_left = image[top:bottom, left:right]
    top_middle = image[top:bottom, right:2*right]
    top_right = image[top:bottom, 2*right:width]
    bottom_left = image[bottom:height, left:right]
    bottom_middle = image[bottom:height, right:2*right]
    bottom_right = image[bottom:height, 2*right:width]

    if index[0] < right and index[1] < bottom:
        print('top left')
        pyautogui.keyDown('space') #Play Pause
        pyautogui.keyUp('space')
    elif index[0] < 2*right and index[1] < bottom:
        print('top middle')
        pyautogui.hotkey('ctrl', 'left')  # Simulate Ctrl + left Arrow #Early track
    elif index[0] < right and index[1] > top:
        print('bottom left')
        pyautogui.hotkey('ctrl','l')  #
    elif index[0] < 2*right and index[1] < 2*bottom:
        print('bottom middle')
        pyautogui.hotkey('ctrl', 'down') #Volume down 
    elif index[0] > right and index[1] < bottom:
        print('top right')
        pyautogui.hotkey('ctrl','right') #Next Track
        # Perform action for top right partition
    elif index[0] > right and index[1] > bottom:
        print('bottom right')
        pyautogui.hotkey('ctrl','up') #Volume up
     

    # # Display the divided screen
    # cv2.imshow('Top Left', top_left)
    # cv2.imshow('Top Right', top_right)
    # cv2.imshow('Bottom Left', bottom_left)
    # cv2.imshow('Bottom Right', bottom_right)

def camera_control():
    while cap.isOpened():
        success, image = cap.read()
        image = cv2.flip(image, 1)  # Flip the image horizontally
        
        if not success:
            print("Ignoring empty camera frame.")
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                data1 = hand_landmarks.landmark[8]
                data2 = hand_landmarks.landmark[4]
                coords1 = mp_drawing._normalized_to_pixel_coordinates(data1.x, data1.y, width, height)
                coords2 = mp_drawing._normalized_to_pixel_coordinates(data2.x, data2.y, width, height)
                cv2.circle(image, coords1, 10, (0, 255, 255), -1)
                try:
                    action_handler(image, coords1, coords2)
                except Exception as e:
                    print(e)
          # Divide the screen into half horizontally
        cv2.line(image, (0, int(height / 2)), (int(width), int(height / 2)), (255, 255, 255), 2)

        # Create two vertical lines to divide the half horizontally into three equal parts
        cv2.line(image, (int(width / 3), 0), (int(width / 3), int(height)), (255, 255, 255), 2)
        cv2.line(image, (int(2 * width / 3), 0), (int(2 * width / 3), int(height)), (255, 255, 255), 2)
       
    
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    camera_control()
