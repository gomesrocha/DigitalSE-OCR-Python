import os
import pytesseract
import cv2
from timeit import default_timer as timer
import time

class Text_Extract:
    def extract_information(self, filename):
        t = time.process_time()
        image = cv2.imread(filename)
        imageg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (i1, i2) = cv2.threshold(imageg, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        options = ""
        text = pytesseract.image_to_string(i2, config=options)
        elapsed_time = time.process_time() - t
        print(elapsed_time)
        return text