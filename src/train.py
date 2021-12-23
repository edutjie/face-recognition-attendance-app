import cv2, os, sqlite3
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(os.path.dirname(BASE_DIR), "images")

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


y_labels, x_train = [], []


def train_face():
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)

                # get the file name
                label = os.path.basename(root).replace(" ", "-").lower()

                # get the user id
                cur = con.cursor()
                user_id = [
                    id[0]
                    for id in cur.execute(
                        "SELECT id FROM users WHERE username = ?", [label]
                    )
                ]

                # open image with pillow and convert it to grayscale
                pil_img = Image.open(path).convert("L")

                # convert pillow imgae to numpy array
                img_array = np.array(pil_img, "uint8")

                faces = face_cascade.detectMultiScale(
                    img_array, scaleFactor=1.3, minNeighbors=5
                )

                # iterate the coordinate in face to get roi
                for x, y, w, h in faces:
                    roi = img_array[y : y + h, x : x + w]

                    # append roi to the list of training data
                    x_train.append(roi)

                    # append id to the list of labels
                    y_labels.append(user_id)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("face-train.xml")


if __name__ == "__main__":
    ...
