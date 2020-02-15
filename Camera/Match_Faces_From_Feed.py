import face_recognition
import cv2
import numpy as np
import time
from Camera.CameraComs import CameraComs
from Databases.face_encodings_database import FaceEncodingsDatabase as fcd
from Databases.Matches_History import MatchesHistory



class MatchFaceFromFeed:
    FCD = None
    camera_coms = None
    matches_history = None
    logger = None

    def __init__(self, _logger):
        self.logger = _logger
        self.camera_coms = CameraComs(self.logger)
        self.matches_history = MatchesHistory(self.logger)
        self.FCD = fcd(self.logger)

    def get_face_matches(self, frame):

        process_this_frame = False
        process_frequancy = 2
        start_time = time.time()
        elapsed_time = 0

        #while True:

        #frame = self.camera_coms.get_frame()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        if elapsed_time < process_frequancy:
            elapsed_time = time.time() - start_time
        else:
            process_this_frame = True
            start_time = time.time()
            elapsed_time = 0

        # Only process every other frame of video to save time
        #if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(list(self.FCD.known_face_encodings.values()), face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(list(self.FCD.known_face_encodings.values()), face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = list(self.FCD.known_face_names.values())[best_match_index]
                match_id = list(self.FCD.known_face_names.keys())[best_match_index]

            face_names.append(name)

            # Display the results
            returned_ids = []
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if name == "Unknown":
                    id = self.FCD.store_new_encoding(None, "Unknown Person", face_encoding, frame)
                    self.logger.info('Unknown face found. Added to database')
                    self.matches_history.store_ticket(id, None, frame, True)
                else:
                    self.matches_history.store_ticket(best_match_index + 1, None, frame, True)
                    self.logger.info('face with id: ' +  str(match_id) +' name: ' + name + ' found.')
                    id = match_id
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name + ' id: ' + str(id), (left + 6, bottom - 6), font, 1.0,
                            (255, 255, 255), 1)
                # Draw a box around the face
                # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                #
                # # Draw a label with a name below the face
                # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

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

            process_this_frame = False

            # Display the resulting image
            #cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break

    # Release handle to the webcam
    cv2.destroyAllWindows()