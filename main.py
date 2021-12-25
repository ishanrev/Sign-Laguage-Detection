import math
def WebCam():
    drawingModule = mp.solutions.drawing_utils
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                          max_num_hands=1,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
    hands_second = mpHands.Hands(static_image_mode=False,
                          max_num_hands=1,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
    web_cam = cv.VideoCapture(0, cv.CAP_DSHOW)  # 0 specifies python to use the first connected camera in
    cam_window = "camera"  # case of multiple connected we cams
    only_hand = "only hand image"
    if not web_cam.isOpened():
        raise IOError("Cannot open webcam")
    while True:
        ret, frame = web_cam.read()
        if not ret:
            print("error")
        else:

            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            result = hands.process(frame)

            if result.multi_hand_landmarks:

                pointCoord = findCoords(frame, result).copy()
                only_hand = cropFrame(frame, pointCoord)
                only_hand = cv.cvtColor(only_hand, cv.COLOR_RGB2BGR)
                #cv.imshow("handlol",only_hand)
                #cv.imshow("hi", only_hand)

                only_hand_result = hands_second.process(cv.cvtColor(only_hand, cv.COLOR_BGR2RGB))
                only_hand_coords = findCoords(only_hand, only_hand_result).copy()
                '''temp = {}
                y , x, h = only_hand.shape
                for key in only_hand_coords.keys():
                    temp[key] = (only_hand_coords[key][0]/x,only_hand_coords[key][1]/y)
                print(temp)'''
                for hand in result.multi_hand_landmarks:
                    drawingModule.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)
                check_match(only_hand,only_hand_coords, mpHands)

                '''print(only_hand_coords)
                #cv.imshow("hand", only_hand)'''
                '''if match == True:
                    print("matched")'''


            new_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
            cv.imshow(cam_window, new_frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    web_cam.release()
    cv.destroyAllWindows()


def findCoords(frame_temp, result):
    """ for mediapipe to be able to process your hands, they must be in the RGB format or it won't work"""
    #frame = frame_temp.copy()
    '''frame = cv.cvtColor(frame_temp, cv.COLOR_BGR2RGB)
    mpHands_new = mp.solutions.hands
    hands_new = mpHands_new.Hands(static_image_mode=False,
                          max_num_hands=1,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
    result = hands_new.process(frame)

    # print(result.multi_hand_landmarks)'''
    pointCoord = {}
    if result.multi_hand_landmarks:
        landmarks = []
        for hand in result.multi_hand_landmarks:
            for cp, handPoint in enumerate(hand.landmark):
                y, x, z = frame_temp.shape
                #print(cp,':(', handPoint.x,',',handPoint.y,')')
                pointCoord[cp] = ((int)(handPoint.x * x), (int)(handPoint.y * y))

    else:
        print("error results are empty")

    return pointCoord


def check_match(only_hand, only_hand_coords_par, HAND):
    only_hand_coords = only_hand_coords_par.copy()
    test_sign, test_sign_coords = Test(only_hand)
    if test_sign_coords == {}:
        print("failed")
        return
    #print(only_hand_coords)
    #print(test_sign_coords)
    distances = {}
    hand_y, hand_x = only_hand.shape[0], only_hand.shape[1]
    test_y, test_x = test_sign.shape[0], test_sign.shape[1]
    possible_test_pixel_location = {}
    for i in test_sign_coords.keys():
        x = (test_sign_coords[i][0] / test_x) * hand_x
        y = (test_sign_coords[i][1] / test_y) * hand_y
        possible_test_pixel_location[i] = (x,y)
        #print(test_sign_coords[i],'changed to', possible_test_pixel_location[i])

    tester_hand = only_hand.copy()
    if possible_test_pixel_location is not None:
        for i in possible_test_pixel_location.keys():
            x_ = int(possible_test_pixel_location[i][0])
            y_ = int(possible_test_pixel_location[i][1])
            d = (x_,y_)
            tester_hand = cv.circle(tester_hand, d, 5, (255, 0, 0), -1)
            try:
                xd = only_hand_coords.get(i)[0]
            except TypeError:
                xd = 0
            try:
                yd = only_hand_coords.get(i)[1]
            except TypeError:
                yd = 0
            d = (xd, yd)
            tester_hand = cv.circle(tester_hand, d, 5, (0, 0, 255), -1)
    cv.imshow("possible coordinates", tester_hand)
    normalized_distances = {}
    for i in only_hand_coords.keys():
        x_dif = pow((only_hand_coords[i][0] - possible_test_pixel_location[i][0]), 2)
        y_dif = pow((only_hand_coords[i][1] - possible_test_pixel_location[i][1]), 2)
        temp = (int)(math.sqrt(x_dif + y_dif))
        distances[i] = temp
        normalized_distances[i] = (temp / (only_hand.shape[0] * only_hand.shape[1]))

    '''mainly checking for which palm beqgins here'''

    print(normalized_distances)
    print()


def processHands():
    pass


def cropFrame(framed, point_dict):  # {point_index : pixel value}
    if (len(point_dict.keys()) == 0):
        raise IOError("coordinates are empty for cropping")
    xcoords = []
    ycoords = []
    frame = framed.copy()
    for key in point_dict.keys():
        xcoords.append(point_dict[key][0])
        ycoords.append(point_dict[key][1])
    max_x = max(xcoords)
    max_y = max(ycoords)
    min_x = min(xcoords)
    min_y = min(ycoords)
    converter = [max_y, max_x, min_y, min_x]
    for v in range(len(converter)):
        if converter[v] < 0:
            converter[v] = 0
    max_y, max_x, min_y, min_x = converter[0], converter[1], converter[2], converter[3]
    if max_y > 480:
        max_y = 479
    if max_x > 640:
        max_x = 639
    # print(frame.shape)
    cropped_image = frame[min_y:max_y, min_x:max_x]
    #
    # print(max_x, max_y, min_x, min_y)
    # cv.circle(frame, (min_x,min_y))
    '''if cropped_image is not None:
        cv.imshow("new window", cv.cvtColor(cropped_image, cv.COLOR_RGB2BGR))'''
    only_hand = cropped_image
    return only_hand

def check_match_hash():
    pass

def Test(final_hand):
    # import cv2 as cv
    mpHands = mp.solutions.hands
    hands_new = mpHands.Hands(static_image_mode=False,
                          max_num_hands=1,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
    '''mpHands = mp.solutions.hands
    win = "win"
    #cv.imshow(win, image)

    drawingModule = mp.solutions.drawing_utils
    frame = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    result = hands.process(frame)
    #print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        landmarks = []
        for hand in result.multi_hand_landmarks:
            pointCoord = {}
            for cp, handPoint in enumerate(hand.landmark):
                y, x, z = frame.shape
                pointCoord[cp] = ((int)(handPoint.x * x), (int)(handPoint.y * y))
            #print(pointCoord)
            only_sign = cropFrame(frame, pointCoord)
            only_sign = cv.resize(only_sign, (final_hand.shape[1],final_hand.shape[0]))
            only_sign_coords = findCoords(only_sign)
            drawingModule.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)'''

    path = r"C:\Users\WMI CONSTRUCTION\Desktop\sign(v)new.jpg"
    image = cv.imread(path)
    newSize = (final_hand.shape[1],final_hand.shape[0])
    ''', cv.INTER_NEAREST'''
    #resizing the goddamn image is the problem
    #print(image.shape)
    #cv.imshow("haha", image)
    #image =
    image = cv.resize(image,newSize)
    result_test = hands_new.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    if result_test.multi_hand_landmarks is None:
        print("ffs man")
    only_sign = image

    only_sign_coords = findCoords(only_sign, result_test)

    return only_sign, only_sign_coords


def ResizingTest():
    mpHands = mp.solutions.hands
    hands_new = mpHands.Hands(static_image_mode=False,
                              max_num_hands=1,
                              min_detection_confidence=0.5,
                              min_tracking_confidence=0.5)
    path = r"C:\Users\WMI CONSTRUCTION\Desktop\sign(v)new.jpg"
    image = cv.imread(path)
    #image = cv.resize()
    h = (image.shape[1]+120, image.shape[0]+100)
    print(h)
    '''result_old = hands_new.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    if result_old.multi_hand_landmarks is None:
        print('result failed')
    else:
        print('succeeded')'''
    image = cv.resize(image, h)
    result = hands_new.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    print(type(result.multi_hand_landmarks))
    if result.multi_hand_landmarks is None:
        print('result failed')
    else:
        print('succeeded')
        landmarks = []
        for hand in result.multi_hand_landmarks:
            pointCoord = {}
            for cp, handPoint in enumerate(hand.landmark):
                y, x, z = image.shape
                pointCoord[cp] = ((int)(handPoint.x * x), (int)(handPoint.y * y))
            print(pointCoord)
    name = "win"
    while True:
        cv.imshow(name, image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()


if __name__ == '__main__':
    import cv2 as cv
    import mediapipe as mp

    #WebCam()
    ResizingTest()
''' os, osc = Test()
    print("shape", os.shape)
    print(osc)
    while True:
        cv.imshow("new", os)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()
'''
    # ResizingTest()
