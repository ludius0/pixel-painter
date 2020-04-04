from tkinter import *
from tkinter import colorchooser
from PIL import ImageGrab
from datetime import datetime
import webbrowser

# Set default values
height = 600
width = 600
c = 10  # constant
pixel_size = 1
color = "black"
pixelBrush = True
pixelEraser = False
fillBucket = False
colorPicker = False

bindSet = {"Color Palette": "c", "Pixel brush": "b", "Eraser": "e", "Bucket": "f", "Color Pickup": "p", "Save": "s"}

# Create background grid (with rows and columns) to know colors for pixels
backGrid = []
for i in range(int(height/c)):
    backGrid.append([])
    for j in range(int(width/c)):
        backGrid[i].append(["white"])


# Set functions
def paint(event): # Draw pixels
    global color, backGrid, pixelBrush, pixelEraser, fillBucket, colorPicker
    
    for i in range(pixel_size):     # Get right size of pixel from invisible grid for coordinations
        x = event.x -(event.x % c)
        y = event.y -(event.y % c)

        x, y = check_back_grid(x, y) # Check for edges

        a = int(y/c) # rows
        b = int(x/c) # columns
        
        # x is width and y is height -> y = rows, y = columns for background grid

        # Choose tool
        if pixelBrush == True:     
            canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color, outline=color) # Tkinter add one pixel up -> that is why, there is "-1"
            backGrid[a][b] = color   # Change color in background grid

        elif fillBucket == True:
            fill_logic(x, y, a, b)
            pixelBrush = True
            fillBucket = False
            pixelEraser = False
            colorPicker = False

        elif colorPicker == True:
            color = backGrid[int(y/c)][int(x/c)]
            pixelBrush = True
            fillBucket = False
            pixelEraser = False
            colorPicker = False
            
            update_square()

        elif pixelEraser == True:
            color_ = "white"
            canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color_, outline=color_)
            backGrid[int(y/c)][int(x/c)] = color_
            

def fill_logic(x, y, a, b):
    global backGrid
    storedPos = [] # stored positions for loop
    
    color2 = backGrid[a][b] # color which will be replaced
    canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color, outline=color)
    backGrid[a][b] = color

    storedPos.append((a, b, x, y))

    check_fill_loop(color2, storedPos, x, y)

def check_fill_loop(color2, storedPos, x, y):
    global backGrid
    num = 0
    while num != len(storedPos):
        a = storedPos[0][0]
        b = storedPos[0][1]
        nx = storedPos[0][2]
        ny = storedPos[0][3]
        status = True

        if ny < (height-c): # make sure it won't go beyond edges
                if backGrid[a+1][b] == color2: #Lower pixel
                    canvas.create_rectangle(nx, ny+c, nx+c-1, ny+c+c-1, fill=color, outline=color)
                    backGrid[a+1][b] = color
                    storedPos.append((a+1, b, nx, ny+c))
                    
        if ny > c:
                if backGrid[a-1][b] == color2: #Upper pixel
                    canvas.create_rectangle(nx, ny-c, nx+c-1, ny-c+c-1, fill=color, outline=color)
                    backGrid[a-1][b] = color
                    storedPos.append((a-1, b, nx, ny-c))

        if nx < (width-c):
                if backGrid[a][b+1] == color2: #Right pixel
                    canvas.create_rectangle(nx+c, ny, nx+c+c-1, ny+c-1, fill=color, outline=color)
                    backGrid[a][b+1] = color
                    storedPos.append((a, b+1, nx+c, ny))

        if nx > c:
                if backGrid[a][b-1] == color2: #Left pixel
                    canvas.create_rectangle(nx-c, ny, nx-c+c-1, ny+c-1, fill=color, outline=color)
                    backGrid[a][b-1] = color
                    storedPos.append((a, b-1, nx-c, ny))

        if status == True:
            del storedPos[0]    

            
def check_back_grid(x, y): # Correcting grid (setting edges)
    if x == 0:
        x = c
    elif y == 0:
        y = c
    elif x == 0 and y == 0:
        x = c
        y = c
    elif (x == width or x == (width+c)) and (y == height or y == (height+c)):
        x = width - c
        y = height - c
    elif x == width or x == (width+c):
        x = width - c
    elif y == height or y == (height+c):
        y = height - c
    return x, y
    

def update_square():
    global label1, color
    label1.destroy()  
    label1 = Label(root, text="    ", bg=color, fg=color)
    label1.pack(side=RIGHT, padx=3)
        
                
# Set brushes            
def ask_color(event): # Ask for colors
    global color
    color = colorchooser.askcolor()
    color = color[-1]           # Choose hex color
    update_square()


def set_brush(event):
    global pixelBrush, pixelEraser, fillBucket, colorPicker
    pixelBrush = True
    pixelEraser = False
    fillBucket = False
    colorPicker = False

def eraser(event): # Set color to white
    global pixelEraser, pixelBrush, fillBucket, colorPicker
    pixelEraser = True
    pixelBrush = False
    fill_bucket = False
    colorPicker = False

def set_fill(event):
    global pixelBrush, pixelEraser, fillBucket, colorPicker
    fillBucket = True
    pixelBrush = False
    pixelEraser = False
    colorPicker = False

def color_picker(event):
    global pixelBrush, pixelEraser, fillBucket, colorPicker
    colorPicker = True
    fillBucket = False
    pixelBrush = False
    pixelEraser = False


# Secondary functions
def callback(url):
    webbrowser.open_new(url)

def get_info(event):
    root2 = Tk()
    
    author = Label(root2, text="Programmed by Ludius0", fg="#95a5a6")
    author.pack(side=BOTTOM)
    author.bind("<Button-1>", lambda e: callback("https://github.com/ludius0"))


    tx1 = "Shortcuts:\n'b' for Pixel brush\n'e' for Eraser\n'f' for Bucket\n'p' for Pick Color\n'c' for Color Palette\n's' for Saving Image\n\n"
    tx2 = "Warning:\nDon't try to be reckless (specialy with bucket), because tkinter may not withstand it and crash program.\n\n"
    text1 = Text(root2, fg="#95a5a6")
    text1.insert(END, tx1)
    text1.insert(END, tx2)
    text1.pack(side=TOP)
    text1.config(state=DISABLED)

    try:
        root2.wm_iconbitmap("icon/icon.ico")
    except TclError:
        print("No ico file found")

def screenshot(event):
    global canvas
    x= root.winfo_rootx() + canvas.winfo_x()
    y= root.winfo_rooty() + canvas.winfo_y()
    x1= x + canvas.winfo_width()
    y1= y + canvas.winfo_height()
    image = ImageGrab.grab((x+c,y+c,x1-c,y1-c))
    image.save(f"images/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.png")

def restart(event):
    global root
    root.destroy()
    window()

def window():
    global root, canvas, label1
    # Set up tkinter module
    root = Tk()
    root.title("Pixel painter by ludius0")
    root.geometry(f"{width+c+c}x{height+100}")
    root.config(bg="#ecf0f1")
    root.resizable(width=False, height=False)


    canvas = Canvas(root, width=width, height=height, bg="white", borderwidth=2)
    canvas.bind("<B1-Motion>", paint)
    canvas.bind("<Button-1>", paint)
    canvas.bind_all(bindSet["Color Palette"], ask_color)
    canvas.bind_all(bindSet["Pixel brush"], set_brush)
    canvas.bind_all(bindSet["Eraser"], eraser)
    canvas.bind_all(bindSet["Bucket"], set_fill)
    canvas.bind_all(bindSet["Color Pickup"], color_picker)
    canvas.bind_all(bindSet["Save"], screenshot)
    canvas.pack(side=TOP)


    button1 = Button(root, text="Pixel brush")
    button1.bind("<Button-1>", set_brush)
    button1.pack(side=LEFT, padx=3)

    button2 = Button(root, text="Eraser")
    button2.bind("<Button-1>", eraser)
    button2.pack(side=LEFT, padx=3)

    button3 = Button(root, text="Bucket")
    button3.bind("<Button-1>", set_fill)
    button3.pack(side=LEFT, padx=3)

    button4 = Button(root, text="Pick Color")
    button4.bind("<Button-1>", color_picker)
    button4.pack(side=LEFT, padx=3)

    button6 = Button(root, text="Color Palette")
    button6.bind("<Button-1>", ask_color)
    button6.pack(side=RIGHT, padx=3)

    button7 = Button(root, text="Info")
    button7.bind("<Button-1>", get_info)
    button7.pack(side=LEFT, padx=3)

    button8 = Button(root, text="Restart")
    button8.bind("<Button-1>", restart)
    button8.pack(side=LEFT, padx=3)

    label1 = Label(root, text="     ", bg=color, fg=color)
    label1.pack(side=RIGHT, padx=3)


    try:
        root.wm_iconbitmap("icon/icon.ico")
        root.mainloop()
    except TclError:
        print("No ico file found")

window()
