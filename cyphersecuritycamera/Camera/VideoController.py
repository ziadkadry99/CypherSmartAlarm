import time

from cyphersecuritycamera.Camera.CameraComs import CameraComs
from cyphersecuritycamera.Camera.Match_Faces_From_Feed import MatchFaceFromFeed
from cyphersecuritycamera.Databases.settings import settings
class Video_Controller:

    def __init__(self):
        self.camera_coms = CameraComs()
        self.face_recognition = MatchFaceFromFeed()
        self.timer = time.time()
        self.Settings = settings()
        # IN SETTINGS
        self.interval_between_detection = int(self.Settings.find_setting_by_name('detection_interval_second')) / 60

    def get_processed_frame(self):
        if time.time() - self.timer > self.interval_between_detection:
            self.timer = time.time()
            return self.face_recognition.get_face_matches(self.camera_coms.get_frame())

        else:
            return  self.camera_coms.get_frame()



