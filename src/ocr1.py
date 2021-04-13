import pytesseract
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Caminho da imagem para o OCR")
ap.add_argument("-d", "--digits", type=int, default=1, help="tipos de digitos")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

options = ""
if args["digits"] > 0:
    options = "outputbase digits"
text = pytesseract.image_to_string(rgb, config=options)
print(text)
