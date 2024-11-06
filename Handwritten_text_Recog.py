import cv2
import pytesseract
from PIL import Image
from tkinter import *
from tkinter import filedialog
import numpy as np
import pyttsx3  # Library for text-to-speech conversion

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def browseFiles():
    global result
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filename:
        # Read the image with OpenCV
        img = cv2.imread(filename)
 
        # Convert to gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
 
        # Write image after noise removal (optional)
        cv2.imwrite("removed_noise.png", img)
 
        # Recognize text with Tesseract
        result = pytesseract.image_to_string(img)
        label_file_explorer.configure(text=result)

def text_to_speech():
    global result
    if result:  # Check if result contains text
        engine.say(result)
        engine.runAndWait()
    else:
        print("No text available for speech conversion.")

window = Tk()

# Set window title and size
window.title('File Explorer')
window.geometry("700x350")
window.config(background="white")

# Header label
reg_info = Label(window, text="Handwritten Text Recognition Using Pytesseract",
                 width='80', height='2', font=("Arial", 12, "bold"), fg="black", bg='lightgrey')
reg_info.place(x=370, y=18, anchor='center')

# Output label
label_file_explorer = Label(window, text="See the Output Here",
                            font=("Arial", 10, "bold"), width=90, height=12, fg="blue")
label_file_explorer.place(x=0, y=35)

# Browse button
button_explore = Button(window, text="Browse Files", fg="white", bg="black",
                        font=("Arial", 10, "bold"), width=10, command=browseFiles)
button_explore.place(x=250, y=270)

# Text-to-Speech button
button_speak = Button(window, text="Convert Text to Speech", fg="white", bg="black",
                      font=("Arial", 10, "bold"), width=20, command=text_to_speech)
button_speak.place(x=370, y=270)

text = Label(window, text="(Select an image)", bg="white", fg="black", font=("Arial", 8, "bold"))
text.place(x=242, y=300)

window.mainloop()