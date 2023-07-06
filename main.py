from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
ps = []
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    # hands, img = detector.findHands(img, draw=False)  # with draw
    hands, _  = detector.findHands(img, draw=False)  # without draw

    pp = None
    for p in ps:
        cv2.circle(img, p, 5, (0,255,0))
        if pp != None:
            cv2.line(img, pp, p, (0,255,0), 5)

        pp = p

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        bb = bbox1
        to = [bb[2:][i] + x for i, x in enumerate(bb[:2])]
        print(handType1, lmList1)
        cv2.rectangle(img, bb[:2], to, (255,0,0), 2)
        # for i, lm in enumerate(lmList1):
        #     pos = lm[:2]
        #     cv2.circle(img, pos, 5, (255,100,0))
        #     cv2.putText(img, str(i), pos, cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))

        pointer = lmList1[8][:2]
        cv2.circle(img, pointer, 10, (255,255,0))

        ps.append(pointer)
        if len(ps) > 100:
            ps.pop(0)




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
