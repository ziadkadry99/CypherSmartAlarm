import face_recognition
# import pickle
from Visuals_Processing.image_utils import ImageUtils
from Databases.Database_Coms import DatabaseComs
import numpy as np



database_coms = DatabaseComs()
image_utils = ImageUtils()

class FaceEncodingsDatabase:
    known_face_encodings = {}
    known_face_names = {}
    logger = None


    def __init__(self, _logger):
        self.logger = _logger
        self.load_database()

    def initialize(self):
        self.load_database()

    def encoding_from_image(self, image_path):
        input_image = face_recognition.load_image_file(image_path)
        input_face_encoding = face_recognition.face_encodings(input_image)[0]
        return input_face_encoding

    def store_new_encoding(self, image_path, name, encoding=None, image=None):
        if image_path:
            encoding = self.encoding_from_image(image_path)
            image = image_utils.get_image_obj(image_path)


        database_coms.exceute_query(''' INSERT INTO encodings(name,encoding,image)
                  VALUES(?,?,?) ''', (name, encoding, image))
        self.logger.debug('New encoding stored.')
        # HIGHLY EXPERIMENTAL
        rows = database_coms.exceute_query(''' SELECT id, name, encoding FROM encodings WHERE encoding=? ''', (encoding.tobytes(),), retRows=True)
        for entry in rows:
            self.known_face_names[entry[0]] = entry[1]
            self.known_face_encodings[entry[0]] = encoding
            # Returns ID
            return entry[0]

    def debug_print_names(self):
        for item in self.known_face_names.items():
            print('id: ',item[0], ' name: ', item[1])

    def get_all_face_encodings(self):
        return self.known_face_encodings

    def get_all_encoding_names(self):
        return self.known_face_names


    def delete_encoding_by_name(self, name):
        if name in self.known_face_names:
            database_coms.exceute_query('DELETE FROM encodings WHERE name=?', (name,))
            id = self.known_face_names.id(name)
            del self.known_face_names [id]
            del self.known_face_encodings[id]
            self.logger.debug('Encoding with ID ' + id + ' Deleted.')
            return True
        return False


    def delete_encoding_by_id(self, id):
        if id <= len(self.known_face_encodings):
            database_coms.exceute_query('DELETE FROM encodings WHERE id=?', (id,))
            del self.known_face_names [id]
            del self.known_face_encodings[id]
            self.logger.debug('Encoding with ID ' + id + ' Deleted.')
            return True
        return False


    def load_database(self):
        if not self.known_face_names:

            rows = database_coms.exceute_query(''' SELECT id, name, encoding FROM encodings ''', retRows=True)
            if rows:
                for entry in rows:
                    spec_xy_np = np.frombuffer(entry[2])
                    self.known_face_names[entry[0]] = entry[1]
                    self.known_face_encodings[entry[0]] = spec_xy_np
                self.logger.info('Encodings database loaded.')
            else:
                self.logger.warning('Encodings database is empty.')
