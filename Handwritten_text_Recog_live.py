import cv2
import pytesseract
from tkinter import *
from PIL import ImageGrab, Image
import numpy as np
import pyttsx3

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the main window
window = Tk()
window.title("Handwritten Whiteboard Recognition")
window.geometry("800x600")

# Global variable to store the recognized text
recognized_text = ""

# Canvas for drawing
canvas = Canvas(window, width=600, height=400, bg="white")
canvas.pack(pady=20)

# Variables to store mouse position for drawing
last_x, last_y = None, None

# Function to capture mouse position on click
def activate_paint(e):
    global last_x, last_y
    last_x, last_y = e.x, e.y

# Function to draw on canvas
def draw(e):
    global last_x, last_y
    x, y = e.x, e.y
    canvas.create_line((last_x, last_y, x, y), fill='black', width=5)
    last_x, last_y = x, y

# Erase function to clear the canvas
def erase_canvas():
    canvas.delete("all")

# Bind mouse events to the canvas
canvas.bind("<Button-1>", activate_paint)
canvas.bind("<B1-Motion>", draw)

# Function to recognize text from the canvas
def translate_text():
    global recognized_text
    # Capture the canvas area
    x = window.winfo_rootx() + canvas.winfo_x()
    y = window.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    # Capture and process the image
    img = ImageGrab.grab().crop((x, y, x1, y1)).convert("L")
    img = np.array(img)
    
    # Image processing for better OCR accuracy
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Recognize text using pytesseract
    recognized_text = pytesseract.image_to_string(img, config='--psm 6')  # PSM 6 is useful for blocks of text
    label_text.configure(text=recognized_text)

# Function to convert recognized text to speech
def text_to_speech():
    global recognized_text
    if recognized_text:
        engine.say(recognized_text)
        engine.runAndWait()
    else:
        label_text.configure(text="No text to convert to speech.")

# Label to display recognized text
label_text = Label(window, text="Recognized Text Will Appear Here", font=("Arial", 12), fg="blue")
label_text.pack(pady=10)

# Translate Button
btn_translate = Button(window, text="Translate", command=translate_text, font=("Arial", 12), bg="black", fg="white")
btn_translate.pack(side=LEFT, padx=10)

# Text-to-Speech Button
btn_speak = Button(window, text="Text to Speech", command=text_to_speech, font=("Arial", 12), bg="black", fg="white")
btn_speak.pack(side=RIGHT, padx=10)

# Erase Button
btn_erase = Button(window, text="Erase", command=erase_canvas, font=("Arial", 12), bg="black", fg="white")
btn_erase.pack(side=LEFT, padx=10)

window.mainloop()
