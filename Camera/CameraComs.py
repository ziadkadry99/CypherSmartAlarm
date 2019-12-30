import cv2


class CameraComs:

    cap = cv2.VideoCapture(0)
    logger = None

    def __init__(self, logger):
        self.logger = logger


    def get_frame(self):
        ret, frame = self.cap.read()
        return frame

    def get_frame_grey(self):
        gray = cv2.cvtColor(self.get_frame(), cv2.COLOR_BGR2GRAY)
        return gray

    def destruct(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.logger.debug('Camera Communication module destructed')

    def get_width(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    def get_height(self):
        return self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        self.cap.release()
