from tkinter import *
from qdollar.recognizer import Gesture,Recognizer, Point
import os

#f = open("template.txt", "w+")
points1 = []
templates1 = []

def paint( event ):
   python_green = "#476042"
   #f.write("Point(%d,%d,%d)," %(event.x,event.y, strokeId))
   points1.append(Point(int(event.x), int(event.y), int(strokeId)))
   x1, y1 = ( event.x - 1 ), ( event.y - 1 )
   x2, y2 = ( event.x + 1 ), ( event.y + 1 )
   w.create_oval( x1, y1, x2, y2, fill = python_green )

def right_click(event):
   global points1
   w.delete('all')
   gesture1 = Gesture("", points1)
   res = Recognizer().classify(gesture1, templates1)
   print("$Q = ",res[0].name, res[1],flush=True)
   points1 = []

def increase_strokeId( e ):
   global strokeId
   strokeId+=1

def addtemplates():
   template1 = Gesture(t1.get(), points1)
   templates1.append(template1)
   w.delete('all')
   t1.delete(0, END)

for filename in os.listdir("templates/"):
   path = os.path.join('templates/',filename)
   f1 = open(path,'r')
   f1 = f1.readlines()
   points1 = []
   for line in f1:
      x,y,strokeId = line.split(" ")
      points1.append(Point(int(x),int(y),int(strokeId)))
   template1 = Gesture(filename, points1)
   templates1.append(template1)

# Tkinter
canvas_width = 500
canvas_height = 300
strokeId = 0


root = Tk()
root.title( "Qdollar" )
w = Canvas(root, 
           width=canvas_width, 
           height=canvas_height)
w.pack(expand = YES, fill = BOTH)
w.bind( "<B1-Motion>", paint )
w.bind("<Button-3>", right_click)
w.bind('<ButtonRelease-1>', increase_strokeId)

message = Label( root, text = "Right Click to identify gesture" )
message.pack( side = BOTTOM )
b1 = Button(root, text = "Add to Templates", command=addtemplates)
b1.pack(side = BOTTOM)

t1 = Entry(root)
t1.pack()
    
mainloop()