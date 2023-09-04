import face_recognition
import os

class FaceRecognition:
    def __init__(self, known_faces_dir):
        self.known_faces_dir = known_faces_dir
        self.known_faces = {}
        self.load_known_faces()

    def load_known_faces(self):
        for filename in os.listdir(self.known_faces_dir):
            name = os.path.splitext(filename)[0]
            image_path = os.path.join(self.known_faces_dir, filename)
            face_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_faces[name] = face_encoding

    def recognize_faces(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(list(self.known_faces.values()), face_encoding)
            name = "Necunoscut"

            if True in matches:
                matched_index = matches.index(True)
                name = list(self.known_faces.keys())[matched_index]

            names.append(name)

        return names
