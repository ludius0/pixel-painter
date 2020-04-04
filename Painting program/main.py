from tkinter import *
from tkinter import colorchooser

# Set default values
height = 600
width = 600
c = 10  # constant
pixel_size = 1
color = "black"
pixelBrush = True
fillBucket = False
# Create background grid (with rows and columns) to know colors for pixels
backGrid = []
for i in range(int(height/c)):
    backGrid.append([])
    for j in range(int(width/c)):
        backGrid[i].append(["white"])


# Set functions
def paint(event): # Draw pixels
    global backGrid, pixelBrush, fillBucket
    
    for i in range(pixel_size):
        x = event.x -(event.x % c)
        y = event.y -(event.y % c)

        x, y = check_back_grid(x, y) # Check for edges
        
        if pixelBrush == True:     
            canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color, outline=color) # Tkinter add one pixel up -> that is why, there is "-1"
            backGrid[int(x/c)][int(y/c)] = color   # Change color in background grid

        elif fillBucket == True:
            color2 = backGrid[int(x/c)][int(y/c)] # temporaly color
            canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color, outline=color)
            backGrid[int(x/c)][int(y/c)] = color
            a = int(x/c)
            b = int(y/c)
            if backGrid[a+1][b] == color2: #Lower pixel
                canvas.create_rectangle(x, y+c, x+c-1, (y+c)+c-1, fill=color, outline=color)
                backGrid[a+1][b] = color
                
            if backGrid[a-1][b] == color2: #Upper pixel
                canvas.create_rectangle(x, y-c, x+c-1, (y-c)+c-1, fill=color, outline=color)
                backGrid[a-1][b] = color
                
            if backGrid[a][b+1] == color2: #Right pixel
                canvas.create_rectangle(x+c, y, (x+c)+c-1, y+c-1, fill=color, outline=color)
                backGrid[a][b+1] = color
                
            if backGrid[a][b-1] == color2: #Left pixel
                canvas.create_rectangle(x-c, y, (x-c)+c-1, y+c-1, fill=color, outline=color)
                backGrid[a][b-1] = color

                
            

def ask_color(event): # Ask for colors
    global color
    key = repr(event.char)
    if key == "'c'":
        color = colorchooser.askcolor()
    color = color[-1]           # Choose hex color

def eraser(event): # Set color to white
    global color, fillBucket
    color = "white"
    fill_bucket = False

def set_brush(event):
    global pixelBrush, fillBucket
    pixelBrush = True
    fillBucket = False

def set_fill(event):
    global pixelBrush, fillBucket
    fillBucket = True
    pixelBrush = False


def check_back_grid(x, y): # Correcting grid
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
    

# Set tkinter module
root = Tk()
root.title("Pixel painter by ludius0")
root.geometry(f"{height+c+c}x{width+c+c}")


canvas = Canvas(root, width=width, height=height, bg='white', borderwidth=2)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<Button-1>", paint)
canvas.bind_all("c", ask_color)
canvas.bind_all("b", set_brush)
canvas.bind_all("e", eraser)
canvas.bind_all("f", set_fill)
canvas.pack(side=TOP)


root.mainloop()
