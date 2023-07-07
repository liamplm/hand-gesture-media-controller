import cv2
import math
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector

from media_player_manager import MediaPlayerManager
from gesture_detection_utils import HandGestureDetector, get_dis

cap = cv2.VideoCapture(0)
hand_detector = HandDetector(detectionCon=0.8, maxHands=1)
face_detector = FaceDetector()
ps = []
player_manager = MediaPlayerManager()

if player_manager.is_failed:
    print('no player found')
    exit(1)

player_pos = player_manager.get_progress()
hand_gesture_detector = HandGestureDetector()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    _, faces = face_detector.findFaces(img, draw=True)
    hands, _  = hand_detector.findHands(img, draw=False)

    player_pos = player_manager.get_progress()
    h, w, _ = img.shape

    hand_gesture_detector.set_size(w, h)

    face_y, face_zone_xs = hand_gesture_detector.handle_faces(faces)
    img = hand_gesture_detector.draw_regions(img, face_y, face_zone_xs)

    hand_gesture_detector.handle_hands(hands, player_manager, face_y, face_zone_xs, img)


    cv2.imshow("img", img)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
