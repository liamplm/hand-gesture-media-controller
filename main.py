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
POINTER_FINGER_ID = 8
THUMB_FINGER_ID = 4
LITTLE_FINGER_ID = 1
MAX_POINTER_THUMB_DIS = 170
is_action_callable = True
pinch_start_pos = [-1,-1]
is_gone_toggle_pause = False
vol = 0
last_pointer_pos = [-1,-1]
# is_pinched = False

hg_detector = HandGestureDetector()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    _, faces = face_detector.findFaces(img, draw=False)
    hands, _  = hand_detector.findHands(img, draw=False)

    player_pos = player_manager.get_progress()
    h, w, _ = img.shape

    hg_detector.set_size(w, h)

    face_y, face_zone_xs = hg_detector.handle_faces(faces)
    img = hg_detector.draw_regions(img, face_y, face_zone_xs)

    hg_detector.handle_hands(hands, player_manager, face_y, face_zone_xs, img)

    # if len(hands) == 1:
    #     hand = hands[0]
    #     landmarks = hand["lmList"]
    #     hand_bb = hand["bbox"]
    #     hand_type = hand["type"]
    #
    #
    #     hand_direction = landmarks[POINTER_FINGER_ID][0] < landmarks[LITTLE_FINGER_ID][0]
    #     hand_direction = hand_direction if hand_type == "Left" else not hand_direction
    #     # When your pinching fingers are more narrow then the other fingers
    #     # and hand is at the right direction (facing camera)
    #     is_command_mode = landmarks[POINTER_FINGER_ID][2] < -10 and \
    #                      hand_direction
    #
    #     pointer = landmarks[POINTER_FINGER_ID][:2]
    #     thumb = landmarks[THUMB_FINGER_ID][:2]
    #
    #     pt_dis = get_dis(pointer, thumb)
    #     # print(pt_dis)
    #
    #     pointer_speed_y = pointer[1] - last_pointer_pos[1]
    #     # print(pointer_speed_y)
    #
    #     # is_looking_pinched = pt_dis < 25 and is_command_mode  
    #     is_pinched = pt_dis < 34 and is_command_mode  
    #     # is_pinched = pt_dis < 30
    #     # is_pinched = is_looking_pinched if is_pinched else is_looking_pinched and abs(pointer_speed_y) < 30
    #     is_higher_then_face = face_y > pointer[1]
    #
    #     if is_pinched:
    #         cv2.circle(img, thumb, 7, (0,255,0), -1)
    #         cv2.circle(img, pointer, 7, (0,255,0), -1)
    #     else:
    #         cv2.circle(img, thumb, 7, (0,255,255), -1)
    #         cv2.circle(img, pointer, 7, (255,255,0), -1)
    # 
    #
    #     if is_pinched and is_action_callable:
    #         pinch_start_pos = pointer
    #         vol = player_manager.player.props.volume
    #         print('pinched')
    #
    #     if is_higher_then_face:
    #         if is_pinched and is_action_callable:
    #             is_gone_toggle_pause = True
    #             is_action_callable = False
    #         elif not is_action_callable and abs(pointer[0] - pinch_start_pos[0]) > 50:
    #             is_gone_toggle_pause = False
    #             vol_move = -(pinch_start_pos[0] - pointer[0]) / (w * 0.7)
    #
    #             new_vol = min(vol + vol_move, 1)
    #             print(f"volume {new_vol:.2f}")
    #             player_manager.set_volume(new_vol)
    #
    #     elif not is_higher_then_face:
    #         is_gone_toggle_pause = False
    #         if is_action_callable:
    #             if face_zone_xs[1] < pointer[0] and is_pinched:
    #                 player_manager.seek(15)
    #                 is_action_callable = False
    #             elif face_zone_xs[0] > pointer[0] and is_pinched:
    #                 player_manager.seek(-15)
    #                 is_action_callable = False
    #
    #
    #     if not is_pinched and is_action_callable == False:
    #         if is_gone_toggle_pause:
    #             player_manager.toggle_pause()
    #         is_action_callable = True
    #         is_gone_toggle_pause = False
    #
    #
    #     last_pointer_pos = pointer


    cv2.imshow("img", img)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
