import cv2
import numpy as np
import pytesseract

def preprocess(image):
    image = cv2.medianBlur(image, 3)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return image

captchaImage = cv2.imread('captcha0.png')

captcha = captchaImage[490:610, 975:1575]

# Add a rectangle around the captcha
cv2.rectangle(captchaImage, (975, 490), (1575, 610), (0, 0, 255), 2)

# Gray scale the image
captchaGray = cv2.cvtColor(captcha, cv2.COLOR_BGR2GRAY)

# remove all black pixels
captchaGray[captchaGray > 1] = 255

# remove all small lines
ret,thresh2 = cv2.threshold(captchaGray,127,255,cv2.THRESH_BINARY_INV)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
opening = 255 - cv2.morphologyEx(thresh2, cv2.MORPH_OPEN, kernel)


# Show the im_result
print(pytesseract.image_to_string(opening, config='--psm 6'))
cv2.imshow('captcha', opening)
cv2.waitKey()