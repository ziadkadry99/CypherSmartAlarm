import cv2
from imutils.video import VideoStream
from cyphersecuritycamera.Databases.settings import settings
from cyphersecuritycamera.Logging.Logger import Logger
class CameraComs:

    logger = Logger()

    def __init__(self):
        print(self.get_connceted_camera_list())
        self.Settings = settings()
        source = int(self.Settings.find_setting_by_name('camera_src'))

        # SRC in settings
        self.cap = VideoStream(src=source).start()


    def get_connceted_camera_list(self):
        cams_test = 10
        camera_list = []
        for i in range(0, cams_test):
            cap = cv2.VideoCapture(i)
            test, frame = cap.read()
            camera_list.append(test)
        return camera_list

    def change_camera_source(self, source_idx):
        # DOESN'T WORK AS INTENDED
        self.cap = VideoStream(src=source_idx).start()

    def get_frame(self):
        frame = self.cap.read()
        return frame

    def get_frame_grey(self):
        gray = cv2.cvtColor(self.get_frame(), cv2.COLOR_BGR2GRAY)
        return gray

    def destruct(self):
        cv2.destroyAllWindows()
        self.logger.debug('Camera Communication module destructed')

    def get_width(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def get_height(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        self.cap.stop()
