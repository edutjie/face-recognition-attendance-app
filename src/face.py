import cv2, os, sqlite3, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# get cascades for frontal face (cascades data taken from BASE_DIR\venv\lib\site-packages\cv2\data)
face_cascade = cv2.CascadeClassifier(
    os.path.join(
        os.path.dirname(BASE_DIR), "cascades/data/haarcascade_frontalface_default.xml"
    )
)


# declare recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# connect to database
con = sqlite3.connect(os.path.join(os.path.dirname(BASE_DIR), "face.db"))


# font settings
font = cv2.FONT_HERSHEY_DUPLEX
text_color = (0, 255, 0)
text_stroke = 2


def take_pictures(username, cam):
    # select webcam
    cap = cv2.VideoCapture(int(cam))
    # count how many pictures we taken
    count = 0
    latest_filename = 0
    image_dir = os.path.join(os.path.dirname(BASE_DIR), "images")
    try:
        os.makedirs(os.path.join(image_dir, username))
    except FileExistsError:
        pass
    image_dir = os.path.join(os.path.dirname(BASE_DIR), f"images/{username}")
    while True:
        # Capture frame by frame
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        # operation on the frame
        # change to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for x, y, w, h in faces:
            # region of interest
            roi_bgr = frame[y : y + h, x : x + w]

            # resize roi
            roi_bgr = cv2.resize(roi_bgr, (200, 200))

            # save image of interest
            img_item = os.path.join(image_dir, f"{latest_filename}.png")
            cv2.imwrite(img_item, roi_bgr)
            latest_filename += 1

            cv2.putText(
                img=roi_bgr,
                text=str(count),
                org=(5, 20),
                fontFace=font,
                fontScale=0.7,
                color=text_color,
                thickness=1,
                lineType=cv2.LINE_AA,
            )

            # increment the number of pictures taken
            count += 1

            # display the frame result
            cv2.imshow("Taking picture...", roi_bgr)

        # break if there's 200 pictures taken
        if count == 200:
            break

        # press Esc to exit program
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # when everything's done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def predict(frame, roi_gray, coordinates: tuple, labels, scanning, username):
    # recognize? deep learning model predict like keras, tf, pytorch, scikit learn
    x, y, w, h = coordinates
    id, pred = recognizer.predict(roi_gray)
    confidence = 100 - pred / 3
    name = labels[id]
    if 63 <= confidence and name == username:
        # print(name)
        cv2.putText(
            img=frame,
            text=name,
            org=(x, y - 10),
            fontFace=font,
            fontScale=1,
            color=text_color,
            thickness=text_stroke,
            lineType=cv2.LINE_AA,
        )
        scanning += 1
    else:
        cv2.putText(
            img=frame,
            text="UNKNOWN",
            org=(x, y - 10),
            fontFace=font,
            fontScale=1,
            color=text_color,
            thickness=text_stroke,
            lineType=cv2.LINE_AA,
        )
    cv2.putText(
        img=frame,
        text=f"{confidence:.2f}",
        org=(x + 10, y + h - 10),
        fontFace=font,
        fontScale=0.4,
        color=text_color,
        thickness=1,
        lineType=cv2.LINE_AA,
    )

    return scanning


def scan_face(username, cam):
    # select webcam
    cap = cv2.VideoCapture(int(cam))

    # get the user id
    cur = con.cursor()
    labels = {
        id: username for id, username in cur.execute("SELECT id,username FROM users")
    }

    # read recognizer
    recognizer.read(os.path.join(os.path.dirname(BASE_DIR), "face-train.xml"))

    scanning, is_success = 0, 0

    # start timer
    start = time.time()

    # select webcam
    while True:
        # Capture frame by frame
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        # operation on the frame
        # change to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        cv2.putText(
            img=frame,
            text=f"{scanning}%",
            org=(10, 30),
            fontFace=font,
            fontScale=1,
            color=text_color,
            thickness=1,
            lineType=cv2.LINE_AA,
        )

        for x, y, w, h in faces:
            # print(x, y, w, h)

            # region of interest (gray)
            roi_gray = gray[y : y + h, x : x + w]
            roi_bgr = frame[y : y + h, x : x + w]

            # resize roi
            roi_gray = cv2.resize(roi_gray, (200, 200))
            roi_bgr = cv2.resize(roi_bgr, (200, 200))

            scanning = predict(
                frame, roi_gray, (x, y, w, h), labels, scanning, username
            )

            # draw box around the region of interest
            box_color = (0, 255, 0)  # BGR
            box_stroke = 2
            # cv2.rectangle(frame, (xcoor_start, ycoor_start), (xcoor_end, ycoor_end))
            cv2.rectangle(
                img=frame,
                pt1=(x, y),
                pt2=(x + w, y + h),
                color=box_color,
                thickness=box_stroke,
            )

        # display the frame result
        cv2.imshow("frame", frame)

        # stop if it scans for more than 50 seconds
        end = time.time()
        if end - start >= 50:
            break

        # check if the scanning is completed
        if scanning == 100:
            is_success = 1
            break

        # press Esc to exit program
        if cv2.waitKey(1) & 0xFF == 27:
            break
    # when everything's done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    return is_success

def available_cam():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else :
            arr.append(index)
            cap.release()
            index += 1
    return arr

if __name__ == "__main__":
    print(available_cam())
    ...
