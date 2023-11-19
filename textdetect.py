import cv2
import pytesseract

#pip install pip install pytesseract
#pip install opencv-python

# Set the path to the Tesseract executable (update this with your installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def text_detection(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    text = pytesseract.image_to_string(blurred)

    print("Detected Text:")
    print(text)

    cv2.imshow("Original Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":

    image_path = 'images.png'
    text_detection(image_path)


