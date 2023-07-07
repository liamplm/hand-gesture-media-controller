import math
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
import cv2

def get_dis(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return math.hypot(x2 - x1, y2 - y1)

cap = cv2.VideoCapture(0)
hand_detector = HandDetector(detectionCon=0.8, maxHands=1)
face_detector = FaceDetector()
ps = []
from media_player_manager import MediaPlayerManager
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
is_pinched = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, faces = face_detector.findFaces(img, draw=False)
    hands, _  = hand_detector.findHands(img, draw=False)

    player_pos = player_manager.get_progress()
    h, w, _ = img.shape
    POS_BAR_Y = 100
    POS_BAR_H = 20
    # POS_BAR_W = int(w * 0.8)
    POS_BAR_W = int(w * 1)
    # pos_bar_padding = int((w - POS_BAR_W) / 2)
    pos_bar_padding = 0
    # cv2.rectangle(img, (pos_bar_padding, int(POS_BAR_Y)), (w - pos_bar_padding, POS_BAR_Y + POS_BAR_H), (200, 255, 255), -1)
    # cv2.circle(img, (pos_bar_padding + int(player_pos * POS_BAR_W), POS_BAR_Y + int(POS_BAR_H / 2)), 10, (50,150,255), -1)
    # cv2.(img, (0, int(h - 50)), (w, h - 30), (255, 200, 255), -1)

    face_y = int(h * 0.3)
    # face_zone_xs = [int(w * 0.4), int(w * 0.6)]
    face_zone_xs = [int(w * 0.5), int(w * 0.51)]
    if len(faces) > 0:
        face = faces[0]
        # print(face)
        face_x, face_y = face['center']
        # x, y, w, h = face['bbox']
        # face_y = face_bb[1]
        # face_y = int(max(0, y + (h/2)))
        # face_zone_xs = [face_bb[0], face_bb[0]+face_bb[2]]


    cv2.line(img, (0,face_y), (w, face_y), (20,200,20), 5)
    # cv2.line(img, (face_x,face_y), (face_x, h), (20,200,20), 5)
    for x in face_zone_xs:
        cv2.line(img, (x,face_y), (x, h), (20,200,20), 5)

    # cv2.line(img, (face_x,face_y), (face_x, h), (20,200,20), 5)

    if len(hands) > 0:

        # Hand 1
        hand = hands[0]
        landmarks = hand["lmList"]  # List of 21 Landmark points
        hand_bb = hand["bbox"]  # Bounding box info x,y,w,h
        hand_type = hand["type"]  # Handtype Left or Right
        # print(landmarks[LITTLE_FINGER_ID], landmarks[POINTER_FINGER_ID])

        to = [hand_bb[2:][i] + x for i, x in enumerate(hand_bb[:2])]
        # cv2.rectangle(img, hand_bb[:2], to, (255,0,0), 2)


        hand_direction = landmarks[POINTER_FINGER_ID][0] < landmarks[LITTLE_FINGER_ID][0]
        # print(hand_direction, hand_type)
        hand_direction = hand_direction if hand_type == "Left" else not hand_direction
        # When your pinching fingers are more narrow then the other fingers
        # and hand is at the right direction (facing camera)
        is_command_mode = landmarks[POINTER_FINGER_ID][2] < -10 and \
                         hand_direction and \
                         1

        for i, lm in enumerate(landmarks):
            pos = lm[:2]
            idx = (i) // 4
            if 1 or i % 4 == 0:
                # print(i, lm)
                # cv2.circle(img, pos, 5, (50,50,255) if idx - 1 > 0 and  fingers[idx - 1] else (50,250,55))
                # cv2.putText(img, f"{idx}-{i}", pos, cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))
                cv2.circle(img, pos, 5, [255 * ((lm[2] + 100) / 200)  for _ in range(3)], -1)
                cv2.putText(img, f"{i}", pos, cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))

        pointer = landmarks[POINTER_FINGER_ID][:2]
        thumb = landmarks[THUMB_FINGER_ID][:2]

        pt_dis = get_dis(pointer, thumb)
        # print(pt_dis)

        pointer_speed_y = pointer[1] - last_pointer_pos[1]
        # print(pointer_speed_y)

        is_looking_pinched = pt_dis < 25 and is_command_mode  
        is_pinched = is_looking_pinched if is_pinched else is_looking_pinched and abs(pointer_speed_y) < 30
        is_higher_then_face = face_y > pointer[1]
        if is_pinched:
            cv2.circle(img, thumb, 10, (0,255,0), -1)
            cv2.circle(img, pointer, 10, (0,255,0), -1)
        # else:
        #     cv2.circle(img, thumb, 7, (0,255,255), -1)
        #     cv2.circle(img, pointer, 7, (255,255,0), -1)
    

        if is_pinched and is_action_callable:
            pinch_start_pos = pointer
            vol = player_manager.player.props.volume
            print('pinched')

        # if abs(pointer[1] - POS_BAR_Y) < 50 and is_pinched:
        if is_higher_then_face:
            if is_pinched and is_action_callable:
                is_gone_toggle_pause = True
                is_action_callable = False
                # pg = (pointer[0] - pos_bar_padding) / POS_BAR_W
                # if 0 <= pg and pg <= 1:
                #     print(pg)
                    # player_manager.set_progress(pg)
            elif not is_action_callable and abs(pointer[0] - pinch_start_pos[0]) > 50:
                is_gone_toggle_pause = False
                vol_move = -(pinch_start_pos[0] - pointer[0]) / (w * 0.7)

                new_vol = min(vol + vol_move, 2)
                print(f"volume {new_vol:.2f}")
                player_manager.set_volume(new_vol)

                # pg = (pointer[0] - pos_bar_padding) / POS_BAR_W
                # if 0 <= pg and pg <= 1:
                #     print(pg)
                #     player_manager.set_progress(pg)
        elif not is_higher_then_face:
            is_gone_toggle_pause = False
            if is_action_callable:
                if face_zone_xs[1] < pointer[0] and is_pinched:
                    player_manager.seek(15)
                    is_action_callable = False
                elif face_zone_xs[0] > pointer[0] and is_pinched:
                    player_manager.seek(-15)
                    is_action_callable = False
            # if face_zone_xs[0] <= pointer[0] and \
            #     pointer[0] <= face_zone_xs[1] and \
            #     is_pinched and \
            #     pinch_start_pos:
            #     # vol = min((pt_dis / MAX_POINTER_THUMB_DIS), 1)
            #     # vol = 1 - ((pointer[1] - face_y) / )
            #     vol_move = (pinch_start_pos[1] - pointer[1]) / ((h - face_y) * 0.7)
            #
            #     # print(f"volume {vol:.2f}", vol_move, pinch_start_pos[1] - pointer[1], (h - face_y))
            #     new_vol = min(vol + vol_move, 2)
            #     print(f"volume {new_vol:.2f}")
            #     player_manager.set_volume(new_vol)
            #     is_action_callable = False
 


        if not is_pinched and is_action_callable == False:
            if is_gone_toggle_pause:
                player_manager.toggle_pause()
            is_action_callable = True
            is_gone_toggle_pause = False



        last_pointer_pos = pointer




        # cv2.line(img, pointer, thumb, (20,200,20), 5)

        # print(landmarks[POINTER_FINGER_ID], landmarks[THUMB_FINGER_ID])
        # z, x, img = detector.findDistance(pointer, thumb, img)  # with draw
        # print(z, x)


        # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw

        # ps.append(pointer)
        # if len(ps) > 100:
        #     ps.pop(0)




        # fingers1 = detector.fingersUp(hand1)

        # if len(hands) == 2:
        #     # Hand 2
        #     hand2 = hands[1]
        #     lmList2 = hand2["lmList"]  # List of 21 Landmark points
        #     bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
        #     centerPoint2 = hand2['center']  # center of the hand cx,cy
        #     handType2 = hand2["type"]  # Hand Type "Left" or "Right"
        #
        #     fingers2 = detector.fingersUp(hand2)

            # Find Distance between two Landmarks. Could be same hand or different hands
            # x = detector.findDistance(lmList1[8], lmList2[8], img)  # with draw
            # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
    # Display
    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
