import cv2
class ImageUtils:
    def get_image_obj(self, img_path):
        return cv2.imread(img_path)