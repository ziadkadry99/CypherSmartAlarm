import face_recognition
import cv2
import numpy as np
from cyphersecuritycamera.Databases.face_encodings_database import FaceEncodingsDatabase as fcd
from cyphersecuritycamera.Databases.Matches_History import MatchesHistory
from cyphersecuritycamera.Databases.settings import settings
from cyphersecuritycamera.Logging.Logger import Logger

class MatchFaceFromFeed:
    FCD = None
    matches_history = None
    logger = Logger()
    Settings = None
    def __init__(self):
        self.matches_history = MatchesHistory()
        self.FCD = fcd()
        self.Settings = settings()

    def get_face_matches(self, frame):



        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            if len(self.FCD.known_face_names.values()) == 0:
                name = "Unknown"
            else:
                matches = face_recognition.compare_faces(list(self.FCD.known_face_encodings.values()), face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(list(self.FCD.known_face_encodings.values()), face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = list(self.FCD.known_face_names.values())[best_match_index]
                    match_id = list(self.FCD.known_face_names.keys())[best_match_index]

            face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if name == "Unknown":
                    # auto_store_new_face will be set here
                    id = self.FCD.store_new_encoding(None, "Unknown Person", face_encoding, frame)
                    self.logger.info('Unknown face found. Added to database')
                    self.matches_history.store_ticket(id, None, frame, True)
                else:
                    self.matches_history.store_ticket(match_id, None, frame, True)
                    self.logger.info('face with id: ' +  str(match_id) +' name: ' + name + ' found.')
                    id = match_id
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                font = cv2.FONT_HERSHEY_DUPLEX
                print(id, 'id')

                # This part will be toggled in settings. draw_box_on_feed = True
                if (int(self.Settings.find_setting_by_name('draw_box_on_feed'))):
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, name + ' id: ' + str(id), (left + 6, bottom - 6), font, 1.0,
                                (255, 255, 255), 1)
                    # Draw a box around the face


                    # add_top = 0
                    # sub_top = 0
                    # add_left = 0
                    # sub_left = 0
                    # if top - 30 > 0:
                    #     sub_top = 30
                    # if top + (bottom - top) + 30 < f_height:
                    #     add_top = 30
                    # if left - 30 > 0:
                    #     sub_left = 30
                    # if left + (right - left) + 30 < f_width:
                    #     add_left = 30
                    # crop_img = frame[top - sub_top:top + (bottom - top) + add_top, left - sub_left:left + (right - left) + add_left]
                    # cv2.imshow("face", crop_img)
        return frame


    # Release handle to the webcam
    cv2.destroyAllWindows()