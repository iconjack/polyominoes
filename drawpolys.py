from polyominoes import polyominos

# https://stackoverflow.com/questions/9886274/how-can-i-convert-canvas-content-to-an-image

try:
   from tkinter import *
except:
   print("Graphic output not available because tkinter is not installed.")
   sys.exit()

try:
    n = int(sys.argv[1])
except:
    n = 5

#  rectangle utility functions inspired from QuickDraw
def offset_rect(rect, dx, dy):
    a, b, c, d = rect
    return [a + dx, b + dy, c + dx, d + dy]

def inset_rect(rect, dx, dy):
    a, b, c, d = rect
    return [a + dx, b + dy, c - dx, d - dy]

margin_left = 50
margin_top = 50
cell_width = cell_height = 20
poly = [(0,0), (1,0), (1,1)]

#  Cells of a polyomino are drawn to the canvas twice, 
#  once with a thicker border and then again with a thinner border.
#  This gives the effect of having a thick border along the perimeter.

def draw_poly(poly, x, y):
    margin_left, margin_top = x, y
    for cell in poly:
        x, y = cell
        rect = [x*cell_width, y*cell_height,
               (x+1)*cell_width, (y+1)*cell_height]
        rect = offset_rect(rect, margin_left, margin_top)
        canvas.create_rectangle(*rect, 
                                fill="red", outline="black", width=3)
        # rect = inset_rect(rect, -2, -2)  ****

    for cell in poly:
        x, y = cell
        rect = [x*cell_width, y*cell_height,
               (x+1)*cell_width, (y+1)*cell_height]
        rect = offset_rect(rect, margin_left, margin_top)
        canvas.create_rectangle(*rect,
                                fill="red", outline="black", width=1)


print(len(list(polyominos(8))))
root = Tk()
root.title("Polyominoes")
canvas = Canvas(root, width=600, height=600, bg="white")
canvas.pack(pady=20)
draw_poly(poly, 10, 20)
root.mainloop(  )

sys.exit()
