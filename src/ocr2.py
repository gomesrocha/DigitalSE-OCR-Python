import pytesseract
import argparse
import cv2
from timeit import default_timer as timer
import time

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Caminho da imagem para o OCR")
ap.add_argument("-d", "--digits", type=int, default=0, help="tipos de digitos")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

options = ""
if args["digits"] > 0:
    options = "outputbase digits"
t = time.process_time()
text = pytesseract.image_to_string(gray, config=options)
elapsed_time = time.process_time() - t
print(elapsed_time)
print(text)
