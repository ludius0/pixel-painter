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
colorPicker = False
# Create background grid (with rows and columns) to know colors for pixels
backGrid = []
for i in range(int(height/c)):
    backGrid.append([])
    for j in range(int(width/c)):
        backGrid[i].append(["white"])


# Set functions
def paint(event): # Draw pixels
    global color, backGrid, pixelBrush, fillBucket, colorPicker
    
    for i in range(pixel_size):     # Get right size of pixel from invisible grid for coordinations
        x = event.x -(event.x % c)
        y = event.y -(event.y % c)

        x, y = check_back_grid(x, y) # Check for edges
        
        # x is width and y is height -> y = rows, y = columns for background grid

        # Choose tool
        if pixelBrush == True:     
            canvas.create_rectangle(x, y, x+c-1, y+c-1, fill=color, outline=color) # Tkinter add one pixel up -> that is why, there is "-1"
            backGrid[int(y/c)][int(x/c)] = color   # Change color in background grid

        elif fillBucket == True:
            fill_logic(x, y)

        elif colorPicker == True:
            color = backGrid[int(y/c)][int(x/c)]
            pixelBrush = True
            fill_bucket = False
            colorPicker = False
            

def fill_logic(x, y):
    global backGrid
    a = int(y/c) # rows
    b = int(x/c) # columns
    storedPos = [] # stored positions for loop
    
    color2 = backGrid[a][b] # temporarily color
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

        if ny < height: # make sure it won't go beyond edges
            if ny != (height-c): #To insure loop out of canvas
                if backGrid[a+1][b] == color2: #Lower pixel
                    canvas.create_rectangle(nx, ny+c, nx+c-1, ny+c+c-1, fill=color, outline=color)
                    backGrid[a+1][b] = color
                    storedPos.append((a+1, b, nx, ny+c))
                    
        if ny > 0:
            if ny != c: # basically (0+c)
                if backGrid[a-1][b] == color2: #Upper pixel
                    canvas.create_rectangle(nx, ny-c, nx+c-1, ny-c+c-1, fill=color, outline=color)
                    backGrid[a-1][b] = color
                    storedPos.append((a-1, b, nx, ny-c))

        if nx < width:
            if nx != (width-c):
                if backGrid[a][b+1] == color2: #Right pixel
                    canvas.create_rectangle(nx+c, ny, nx+c+c-1, ny+c-1, fill=color, outline=color)
                    backGrid[a][b+1] = color
                    storedPos.append((a, b+1, nx+c, ny))

        if nx > 0:
            if nx != c:
                if backGrid[a][b-1] == color2: #Left pixel
                    canvas.create_rectangle(nx-c, ny, nx-c+c-1, ny+c-1, fill=color, outline=color)
                    backGrid[a][b-1] = color
                    storedPos.append((a, b-1, nx-c, ny))

        if status == True:
            del storedPos[0]

        
                
            

def ask_color(event): # Ask for colors
    global color
    key = repr(event.char)
    if key == "'c'":
        color = colorchooser.askcolor()
    color = color[-1]           # Choose hex color

def eraser(event): # Set color to white
    global color, pixelBrush, fillBucket, colorPicker
    color = "white"
    pixelBrush = True
    fill_bucket = False
    colorPicker = False

def set_brush(event):
    global pixelBrush, fillBucket, colorPicker
    pixelBrush = True
    fillBucket = False
    colorPicker = False

def set_fill(event):
    global pixelBrush, fillBucket, colorPicker
    fillBucket = True
    pixelBrush = False
    colorPicker = False

def color_picker(event):
    global pixelBrush, fillBucket, colorPicker
    colorPicker = True
    fillBucket = False
    pixelBrush = False


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
canvas.bind_all("p", color_picker)
canvas.pack(side=TOP)


root.mainloop()
