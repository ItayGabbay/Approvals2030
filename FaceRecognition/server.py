from flask import Flask
from flask import request
import jsonpickle
import face_recognition

app = Flask(__name__)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        images = jsonpickle.loads(request.data)
        img1 = images['face']
        all_images = [face_recognition.face_encodings(x)[0] for x in images['all_faces']]
        result = jsonpickle.dumps(face_recognition.compare_faces(all_images, face_recognition.face_encodings(img1)[0]))
        print(result)
        return result

    elif request.method == 'GET':
        img1 = face_recognition.face_encodings(face_recognition.load_image_file('Carlton_Dotson_0001.jpg'))[0]
        img2 = face_recognition.face_encodings(face_recognition.load_image_file('Carolina_Moraes_0001.jpg'))[0]
        img3 = face_recognition.face_encodings(face_recognition.load_image_file('Carolina_Moraes_0002.jpg'))[0]
        result = face_recognition.compare_faces([img1, img3], img2)
        print(result)
        return str(result)
    else:
        return None
    