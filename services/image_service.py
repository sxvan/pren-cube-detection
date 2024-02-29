import cv2 as cv
import numpy as np

class ImageService:
    def blur_img(self, img, size):
        return cv.blur(img, (size, size))

    def get_angles_of_straight_lines(self, img, threshold):
        angles = []
        contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            epsilon = 0.005 * cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, epsilon, True)

            for i in range(len(approx)):
                x1, y1 = approx[i][0]
                x2, y2 = approx[(i + 1) % len(approx)][0]
                segment_length = cv.norm(np.array([x1, y1]) - np.array([x2, y2]))
                if segment_length > threshold:
                    pitch_rad = np.arctan2(y2 - y1, x2 - x1)
                    pitch_deg = np.degrees(pitch_rad)
                    angles.append(pitch_deg)

        return angles
