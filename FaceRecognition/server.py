from flask import Flask
from flask import request
import face_recognition

app = Flask(__name__)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        images = request.data
        img1 = images[0]
        images = [face_recognition.face_encodings(x) for x in images[1:]]
        return face_recognition.compare_faces(images, img1)

    elif request.method == 'GET':
        img1 = face_recognition.face_encodings(face_recognition.load_image_file('Carlton_Dotson_0001.jpg'))[0]
        img2 = face_recognition.face_encodings(face_recognition.load_image_file('Carolina_Moraes_0001.jpg'))[0]
        img3 = face_recognition.face_encodings(face_recognition.load_image_file('Carolina_Moraes_0002.jpg'))[0]
        result = face_recognition.compare_faces([img1, img3], img2)
        print(result)
        return str(result)
    else:
        return None
    