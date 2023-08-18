''' IMPORTANT PLEASE READ'''
''' PLEASE READ- IF THE CODE IS NOT RUNNING IT IS BECAUSE THE VERSION OF CHROME I HAVE WAS DIFFERENT TO THE VERSION YOU HAVE TO FIX THIS
PLEASE GO TO THIS WEBSITE https://sites.google.com/chromium.org/driver/downloads?authuser=0 AND DOWNLOAD THE CORRECT VERSION YOU CAN CHECK REQUIREMENTS.TXT FILE FOR AN EXPLANATION MAKE SURE TO SET THE DOWNLOAD DIRECTORY TO THE SAME ONE THIS PYTHON FILE IS IN'''

import math
import sys
from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import imageIO.png
import tkinter
from tkinter import *
# import filedialog module
from PIL import Image,ImageDraw, ImageTk
from pyzbar.pyzbar import decode
from tkinter import Tk, Canvas, filedialog
import cv2
from selenium import webdriver
import time

path = "./chromedriver"
driver = webdriver.Chrome(path)

def browseFiles():
    filetypes = (("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"),)
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=filetypes)

    image2 = cv2.imread(filename)
    barcodes2  = decode(image2)
    for barcode in barcodes2:
          barcode_rect = barcode.rect
          cv2.rectangle(image2 , (barcode_rect.left, barcode_rect.top),(barcode_rect.left + barcode_rect.width, barcode_rect.top + barcode_rect.height),(0,0,255),4)
          data = barcode.data.decode("utf-8")
          type = barcode.type
          text = f"{data}, {type}"
          cv2.putText(image2,text,(barcode_rect.left,barcode_rect.top-10),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),2)

    image_pil = Image.fromarray(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
    photo2 = ImageTk.PhotoImage(image_pil)

    label = Label(container,image=photo2).grid(row = 3,column = 1 )
    print(data)
    print("test")
    driver.get('https://www.barcodelookup.com/' + data)
    # Change label contents
    #label_file_explorer.configure(text="File Opened: "+filename)

window  = Tk()
labelText = Label(window, text = "Select an image that contains a barcode and once the image is selected allow a few seconds for it to be processed",font=("Helvetica", 32),bg="grey")
#"*.jpg;*.jpeg;*.png;*.gif;*.bmp"
labelText2 = Label(window, text = "Allowed image types are jpg, jpeg, png, gif and bmp",font=("Helvetica", 32),bg="grey")
labelText.pack()
labelText2.pack()
# screen_width = window.winfo_screenwidth()
# screen_height = window.winfo_screenheight()
# window.minsize(screen_width, screen_height)
button = Button(text = "Select Image", command= browseFiles)
button.configure(width=20, height=2,fg="white", bg="green",font=("Helvetica", 16))
button.pack()
window.title("PNG Image Barcode Scanner")

window.configure(bg="grey")
container = Frame(window)
container.pack()

window.mainloop()
