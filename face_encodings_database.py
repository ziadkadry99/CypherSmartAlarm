import face_recognition
import pickle


known_face_encodings = []
known_face_names = []


def __init__(self):
    self.load_database()

def initialize():
    load_database()

def encoding_from_image(image_path):
    global known_face_names
    global known_face_encodings
    input_image = face_recognition.load_image_file(image_path)
    input_face_encoding = face_recognition.face_encodings(input_image)[0]
    return input_face_encoding

def store_new_encoding(image_path, name, persist = False):
    global known_face_names
    global known_face_encodings
    encoding = encoding_from_image(image_path)
    known_face_encodings.append(encoding)
    known_face_names.append(name)
    if persist:
        persist_changes()


def persist_changes():
    global known_face_names
    global known_face_encodings
    with open("encodings.enc", "wb") as enc:
        pickle.dump(known_face_encodings, enc)
    with open("encodings_names.encn", "wb") as encn:
        pickle.dump(known_face_names, encn)


def debug_print_names():
    global known_face_names
    global known_face_encodings
    print(type(known_face_encodings[0]))
    for name in known_face_names:
        print(name)

def get_all_face_encodings():
    global known_face_encodings
    return known_face_encodings

def get_all_encoding_names():
    global known_face_names
    return known_face_names

def load_database():
    global known_face_names
    global known_face_encodings

    with open("encodings_names.encn", "rb") as encn:
        known_face_names = pickle.load(encn)
    with open("encodings.enc", "rb") as enc:
        known_face_encodings = pickle.load(enc)
