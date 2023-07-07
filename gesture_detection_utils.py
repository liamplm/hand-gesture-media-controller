from typing import Dict, List, Literal, Tuple, TypedDict, Union 
import cv2
import math

## Types
Landmarks = List[Tuple[int, int, int]]
HandType = Literal["Right", "Left"]
# Hand = Dict[Literal["lmList", "bbox", "type"], Union[List, str, int]]
class Hand(TypedDict):
    lmList: Landmarks
    bbox: Tuple[int, int, int, int]
    type: HandType


## Constants
POINTER_FINGER_ID = 8
THUMB_FINGER_ID = 4
LITTLE_FINGER_ID = 17

## Methods
def get_dis(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return math.hypot(x2 - x1, y2 - y1)

class HandGestureDetector:
    def __init__(self) -> None:
        self.last_pointer_pos = [-1,-1]
        self.is_action_callable = True
        self.pinch_start_pos = [-1,-1]
        self.is_gone_toggle_pause = False
        self.vol = 0
        self.last_pointer_pos = [-1,-1]
        self.w = self.h = 0

    def set_size(self, w, h):
        self.w = w
        self.h = h

    def handle_hands(self, hands: List[Hand], player_manager, face_y, face_zone_xs, img):
        if len(hands) != 1:
            return 

        hand = hands[0]
        landmarks = hand["lmList"]
        hand_bb = hand["bbox"]
        hand_type = hand["type"]

        pointer = landmarks[POINTER_FINGER_ID]
        thumb = landmarks[THUMB_FINGER_ID]
        little_finger = landmarks[LITTLE_FINGER_ID]

        self.draw_hand_landmarks(landmarks, img)

        is_pinched, is_higher_then_face = self.check_hand_status(pointer, thumb, little_finger, hand_type, face_y)
        # print('res', is_pinched, is_higher_then_face)

        pointer = landmarks[POINTER_FINGER_ID][:2]
        thumb = landmarks[THUMB_FINGER_ID][:2]
        little_finger = landmarks[LITTLE_FINGER_ID][:2]

        if is_pinched:
            cv2.circle(img, thumb, 7, (0,255,0), -1)
            cv2.circle(img, pointer, 7, (0,255,0), -1)
        else:
            cv2.circle(img, thumb, 7, (0,255,255), -1)
            cv2.circle(img, pointer, 7, (255,255,0), -1)


        if is_pinched and self.is_action_callable:
            self.pinch_start_pos = pointer
            self.vol = player_manager.player.props.volume
            print('pinched')

        if is_higher_then_face:
            if is_pinched and self.is_action_callable:
                self.is_gone_toggle_pause = True
                self.is_action_callable = False
            elif not self.is_action_callable and abs(pointer[0] - self.pinch_start_pos[0]) > 50:
                self.is_gone_toggle_pause = False
                vol_move = -(self.pinch_start_pos[0] - pointer[0]) / (self.w * 0.7)

                new_vol = min(self.vol + vol_move, 1)
                print(f"volume {new_vol:.2f}")
                player_manager.set_volume(new_vol)

        elif not is_higher_then_face:
            self.is_gone_toggle_pause = False
            if self.is_action_callable:
                if face_zone_xs[1] < pointer[0] and is_pinched:
                    player_manager.seek(15)
                    self.is_action_callable = False
                elif face_zone_xs[0] > pointer[0] and is_pinched:
                    player_manager.seek(-15)
                    self.is_action_callable = False


        if not is_pinched and self.is_action_callable == False:
            if self.is_gone_toggle_pause:
                player_manager.toggle_pause()
            self.is_action_callable = True
            self.is_gone_toggle_pause = False


        self.last_pointer_pos = pointer

    def handle_faces(self, faces): 
        face_y = int(self.h * 0.5)
        # face_zone_xs = [int(w * 0.4), int(w * 0.6)]
        face_zone_xs = [int(self.w * 0.5), int(self.w * 0.51)]
        # if len(faces) == 1:
        #     face = faces[0]
        #     _, _face_y = face['center']
        #     face_y = int(face_y *0.95 + _face_y * 0.05)

        return face_y, face_zone_xs

    def draw_regions(self, img, face_y, face_zone_xs):
        cv2.line(img, (0,face_y), (self.w, face_y), (20,200,20), 5)
        for x in face_zone_xs:
            cv2.line(img, (x,face_y), (x, self.h), (20,200,20), 5)

        return img

    def check_hand_status(self, pointer, thumb, little_finger, hand_type: HandType, face_y: int):
        hand_direction = pointer[0] < little_finger[0]
        hand_direction = hand_direction if hand_type == "Left" else not hand_direction

        # When your pinching fingers are more narrow then the other fingers
        # and hand is at the right direction (facing camera)
        is_command_mode = little_finger[2] < -10 and \
                         hand_direction

        # print(little_finger[2], hand_direction, end='\t')


        pt_dis = get_dis(pointer[:2], thumb[:2])

        pointer_speed_y = pointer[1] - self.last_pointer_pos[1]
        # print(pointer_speed_y)

        # print(pt_dis, is_command_mode)
        # is_looking_pinched = pt_dis < 25 and is_command_mode  
        # is_pinched = pt_dis < 34 and is_command_mode  
        is_pinched = pt_dis < 30
        # is_pinched = is_looking_pinched if is_pinched else is_looking_pinched and abs(pointer_speed_y) < 30
        is_higher_then_face = face_y > pointer[1]

        return is_pinched, is_higher_then_face

    def draw_hand_landmarks(self, landmarks: Landmarks, img):
        for i, lm in enumerate(landmarks):
            pos = lm[:2]
            idx = (i) // 4
            if 1 or i % 4 == 0:
                # print(i, lm)
                # cv2.circle(img, pos, 5, (50,50,255) if idx - 1 > 0 and  fingers[idx - 1] else (50,250,55))
                # cv2.putText(img, f"{idx}-{i}", pos, cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))
                cv2.circle(img, pos, 5, [255 * ((lm[2] + 100) / 200)  for _ in range(3)], -1)
                cv2.putText(img, f"{i}", pos, cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))

        return img

