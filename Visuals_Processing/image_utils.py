import cv2
class ImageUtils:

    def get_image_obj(self, img_path):
        return cv2.imread(img_path)

    def crop_bottom_half(image, percentage):
        # Crops from bottom, needs to be a region cropping from the top and bottom
        cropped_img = image[int(image.shape[0] * percentage) : image.shape[0]]
        return cropped_img