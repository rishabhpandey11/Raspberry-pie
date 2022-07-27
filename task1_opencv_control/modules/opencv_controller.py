import logging
import numpy as np
import cv2

USE_FAKE_PI_CAMERA = True    # Chage to FALSE if testing in the Raspberry Pi

if USE_FAKE_PI_CAMERA:
    from .camera import Camera  # For running app
else:
    from .pi_camera import Camera  # For running Raspberry Pi

log = logging.getLogger(
    __name__)  # Creates a logger instance, we use it to log things out


class OpenCVController(object):

    def __init__(self):
        self.current_shape = [False, False, False]
        print('OpenCV controller initiated')

    def process_frame(self):
        camera = Camera()
        frame = camera.get_frame()
        print (type(frame))
        jpg_to_np = np.frombuffer(frame, np.uint8)
        img = cv2.imdecode(jpg_to_np, cv2.COLOR_RGB2BGR)  # coverting jpg to np
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_contour = img.copy()
        # creating mask  so mask and shapes are visible
        lowervalue = np.array([0, 122, 31])
        uppervalue = np.array([179, 255, 237])
        mask = cv2.inRange(hsv_image, lowervalue, uppervalue)
        result_img = cv2.bitwise_and(img, img, mask=mask)

        grayscale_image = cv2.cvtColor(result_img, cv2.COLOR_BGR2GRAY)
        blur_image = cv2.GaussianBlur(grayscale_image, (7, 7), 1)
        canny_image = cv2.Canny(blur_image, 25, 25)
        dilate_image = cv2.dilate(canny_image, kernel=np.ones((2, 2), np.uint8), iterations=1)

        contours, _ = cv2.findContours(dilate_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if 1600 < area < 303000:
                cv2.drawContours(img_contour, contour, -1, (0, 128, 0), 8)
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

                x, y, w, h = cv2.boundingRect(approx)

                if len(approx) == 3:
                    cv2.putText(img_contour, "Triangle", (x + (w//2), y + (y//2)), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 7)

                elif len(approx) == 4:
                    aspectRatio = float(w) / h
                    print(area)
                    if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                        cv2.putText(img_contour, "Square", (x + (w//2), y + (y//2)), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 7)
                    else:
                        cv2.putText(img_contour, "Mark", (x + (w//2), y + (y//2)), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 7)
                        cv2.drawContours(img_contour, contour, -1, (0, 0, 255), 8)

                elif len(approx) >= 4:
                    cv2.putText(img_contour, "Circle", (x + (w//2), y + (y//2)), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 7)
                else:
                    cv2.putText(img_contour, " ", (x + (w//2), y + (y//2)), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 7)

        ret, output_img = cv2.imencode(".jpg",img_contour)
        return output_img.tobytes()

    def get_current_shape(self):
        return self.current_shape
