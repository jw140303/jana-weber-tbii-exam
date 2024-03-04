import tkinter as tk
from PIL import Image, ImageTk

def clear_widgets(root):
    """
    This function clears any widgets that are on the screen to make space for new widgets.
    """
    for i in root.winfo_children():
        i.destroy()

def add_image(root, file_path, width, height):
    """
    This function places a picture on the screen using the pack method.
    """
    global pic, f1, Lab

    f1 = tk.Frame(root)
    img = Image.open(file_path) #reading in the image
    img = img.resize((width, height), Image.LANCZOS) #defining the size of the image
    pic = ImageTk.PhotoImage(img)
    Lab = tk.Label(f1, image=pic, borderwidth = 0)

    #placing the image
    Lab.pack()
    f1.pack(pady = 5)

def add_image_place_method(root, file_path, width, height, xcoordinate, ycoordinate):
    """
    This function places a picture on the screen using the place method.
    The place method allows for a more specific placement on the page than the pack method.
    """
    global pic, f1, Lab

    f1 = tk.Frame(root)
    img = Image.open(file_path) #reading in the image
    img = img.resize((width, height), Image.LANCZOS) #defining the size of the image
    pic = ImageTk.PhotoImage(img)
    Lab = tk.Label(f1, image=pic, borderwidth = 0)

    #placing the image
    Lab.pack()
    f1.place(x = xcoordinate, y = ycoordinate)

def add_sectioning_image(root):
    """
    This function adds a white image to the bottom of the page.
    The picture visually separates the page buttons from the rest of the GUI.
    """
    f2 = tk.Frame(root)
    img2 = Image.open('images/white.png')  #reading in the image
    img2 = img2.resize((800, 75), Image.LANCZOS)  #defining the size of the image
    pic2 = ImageTk.PhotoImage(img2)
    Lab2 = tk.Label(f2, image=pic2)

    #placing the image
    Lab2.pack()
    f2.place(x = 0, y = 520)

#defining some colours and fonts that will used later on
background_colour_1 = '#C0727E'
background_colour_2 = '#873D48'
font_colour_1 = 'white'
font_colour_2 = '#873D48'
heading = 'Georgia 14 bold'
text = 'Georgia 12'

#defining different quotes for the homepage that randomize each time
quotes = ["Haven't drawn in a while? - No worries, you are doing great!",
          "Connecting with people is a great way to learn new things!",
          "Need inspiration? Look at the great artworks your friends have made!",
          "New amazing profiles are waiting to be discovered by you!"]