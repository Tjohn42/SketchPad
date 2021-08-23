# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 14:52:41 2021

@author: johns
"""

import math
from tkinter import *
from tkinter.colorchooser import askcolor
import json
import tkinter.filedialog
from tkinter.filedialog import askopenfilename


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    


    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)
        
        self.rec_button = Button(self.root, text = 'Rectangle', command =self.drawRec)
        self.rec_button.grid(row=0, column=5)
        
        self.oval_button = Button(self.root, text = 'Ellipse', command =self.drawOval)
        self.oval_button.grid(row=0, column=6)

        self.line_button = Button(self.root, text = 'Line', command =self.drawLine)
        self.line_button.grid(row=0, column=7)

        self.square_button = Button(self.root, text = 'Square', command =self.drawSquare)
        self.square_button.grid(row=0, column=8)
        
        self.circle_button = Button(self.root, text = 'Circle', command =self.drawCircle)
        self.circle_button.grid(row=0, column=9)
        
        self.poly_button = Button(self.root, text = 'Polygon', command =self.drawPoly)
        self.poly_button.grid(row=0, column=10)
        
        self.find_button = Button(self.root, text = 'Find', command =self.findItem)
        self.find_button.grid(row=0, column=11)
        
        self.group_button = Button(self.root, text = 'Group', command =self.groupItem)
        self.group_button.grid(row=0, column=12)
        
        self.copy_paste_Button = Button(self.root, text = 'Copy/Paste', command =self.copyPaste)
        self.copy_paste_Button.grid(row=0, column=13)

        self.delete_Button = Button(self.root, text = 'Delete', command =self.DeleteItem)
        self.delete_Button.grid(row=0, column=14)
        
        self.save_Button = Button(self.root, text = 'Save', command =self.saveCanvas)
        self.save_Button.grid(row=0, column=15)
        
        self.load_Button = Button(self.root, text = 'Load', command =self.loadCanvas)
        self.load_Button.grid(row=0, column=16)
        
        self.undo_Button = Button(self.root, text = 'Undo', command =self.undoLast)
        self.undo_Button.grid(row=0, column=17)
        
        self.redo_Button = Button(self.root, text = 'Redo', command =self.redoLast)
        self.redo_Button.grid(row=0, column=18)

        self.selected = None
        self.ovals = {}
        
        self.c = Canvas(self.root, bg='white', width=1000, height=1000)
        self.c.grid(row=1, columnspan=100)
       # self.c.bind("<Button 3>", self.draw_polygons)
       
        self._drag_data = {"x": 0, "y": 0, "item": None}
        
        self.group_drag= {"x": 0, "y": 0, "item": None}
        
        self.copy_data= {"x": 0, "y": 0, "item": None}
        
        self.save_data= {}
        self.save_data['shape'] = []
        
        self.all_data= {}
        self.all_data['All'] = []
        
        self.kinds = [self.c.create_oval, self.c.create_rectangle, self.c.create_line, self.c.create_polygon]

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        

    def use_pen(self):
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def drawOval(self):
        self.shape = self.kinds[0] 
        self.c.bind('<ButtonPress-1>', self.onStart) 
        self.c.bind('<B1-Motion>',     self.onGrow)  
        self.c.bind('<Double-1>',      self.onClear) 
        
    def drawCircle(self):
        self.shape = self.kinds[0] 
        self.c.bind('<ButtonPress-1>', self.onStart) 
        self.c.bind('<B1-Motion>',     self.onGrowPerfect)  
        self.c.bind('<Double-1>',      self.onClear) 

    def drawRec(self):
        self.shape = self.kinds[1] 
        self.c.bind('<ButtonPress-1>', self.onStart) 
        self.c.bind('<B1-Motion>',     self.onGrow)
        self.c.bind('<Double-1>',      self.onClear) 
        #self.c.bind('<ButtonPress-3>', self.onMove)


    def drawSquare(self):
        self.shape = self.kinds[1] 
        self.c.bind('<ButtonPress-1>', self.onStart) 
        self.c.bind('<B1-Motion>',     self.onGrowPerfect)  
        self.c.bind('<Double-1>',      self.onClear) 
        #self.c.bind('<ButtonPress-3>', self.onMove)  
       
    def drawLine(self):
        self.shape = self.kinds[2] 
        self.c.bind('<ButtonPress-1>', self.onStart) 
        self.c.bind('<B1-Motion>',     self.onGrow)  
        self.c.bind('<Double-1>',      self.onClear) 
        
    def drawPoly(self):
        self.shape = self.kinds[3]
        self.line = self.kinds[2]
        self.oval = self.kinds[0]
        self.c.bind('<Button 3>',     self.func_Draw_polygons)  
        self.c.bind('<Double-1>',      self.onClear) 
        
    def findItem(self):
        self.c.bind('<ButtonPress-1>', self.drag_start) 
        self.c.bind('<ButtonRelease-1>', self.drag_stop)
        self.c.bind('<B1-Motion>',     self.drag)
        self.c.bind('<Double-1>',      self.onClear) 
        
    def groupItem(self):
        self.shape = self.kinds[3]
        self.line = self.kinds[2]
        self.oval = self.kinds[0]
        self.c.bind('<ButtonPress-1>', self.groupDrag) 
        self.c.bind('<ButtonRelease-1>', self.drag_stop)
        self.c.bind('<B1-Motion>',     self.dragGroup)
        self.c.bind('<Button 3>', self.unGroup) 
        self.c.bind('<Double-1>',      self.onClear) 
        
    def copyPaste(self):
        self.shape = self.kinds[1]
        self.line = self.kinds[2]
        self.oval = self.kinds[0]
        self.poly = self.kinds[3]
        self.c.bind('<ButtonPress-1>', self.copy) 
        self.c.bind('<Button 3>',     self.paste)
        self.c.bind('<Double-1>',      self.onClear)

    def DeleteItem(self):
        self.c.bind('<ButtonPress-1>', self.deleted)
        self.c.bind('<Double-1>',      self.onClear)
        
    def undoLast(self):
        undoList = self.c.find_all()
        #self.all_data = self.c.find_withtag(undoList[-1])
        self.all_data['All'].append({"location": self.c.coords(undoList[-1]), "size": self.c.bbox(undoList[-1]),
                     "item": self.c.type(undoList[-1]),"fill":self.c.itemconfig(undoList[-1])['fill'][4] })
        self.c.delete(self.c.find_withtag(undoList[-1]))
        
    def redoLast(self):
        self.shape = self.kinds[1]
        self.line = self.kinds[2]
        self.oval = self.kinds[0]
        self.poly = self.kinds[3]
        RedoList = self.all_data['All'][0]
        if RedoList['item'] == "oval":
            objectId = self.oval(RedoList['size'],fill=RedoList['fill'])
            self.drawn = objectId
        elif RedoList['item'] == "rectangle":
            objectId = self.shape(RedoList['size'],fill=RedoList['fill'])
            self.drawn = objectId
        elif RedoList['item'] == "line":
            objectId = self.line(RedoList['location'],fill=RedoList['fill'])
            self.drawn = objectId
        else: 
            numberofPoint=len(RedoList['location'])
            # Draw polygon
            print("num:, ", numberofPoint)
            if numberofPoint>2:
                objectId = self.poly(RedoList['location'],fill=RedoList['fill'])
            elif numberofPoint==2 :
                self.line(list_of_points)
            else:
                pass
            self.drawn = objectId


    
    def saveCanvas(self):
        everything = self.c.find_all()
        for i in everything:
            print(i)
            print( self.c.type(i))
            print( self.c.itemconfig(i))
            print(self.c.bbox(i))
            print(self.c.coords(i))
            print(list_of_points)
           # self.save_data["item"] = self.c.type(i)
            #self.save_data["location"] = self.c.coords(i)
            #self.save_data["size"] = self.c.bbox(i)
            
            self.save_data['shape'].append({"location": self.c.coords(i), "size": self.c.bbox(i), "item": self.c.type(i),
                          "fill":self.c.itemconfig(i)['fill'][4] })
            
            print(self.save_data)
        f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        json.dump(self.save_data,f)
        f.close
        #with open('readme.txt', 'w') as f:
           # json.dump(self.save_data, f)

    def loadCanvas(self):
        self.shape = self.kinds[1]
        self.line = self.kinds[2]
        self.oval = self.kinds[0]
        self.poly = self.kinds[3]
        filename = askopenfilename()
        with open(filename) as json_file:
            data = json.load(json_file)
            for p in data['shape']:
                print(p['item'])
                if p['item'] == "oval":
                    objectId = self.oval(p['size'],fill=p['fill'])
                    self.drawn = objectId
                elif p['item'] == "rectangle":
                    objectId = self.shape(p['size'],fill=p['fill'])
                    self.drawn = objectId
                elif p['item'] == "line":
                    objectId = self.line(p['location'],fill=p['fill'])
                    self.drawn = objectId
                else: 
                    numberofPoint=len(p['location'])
                    # Draw polygon
                    print("num:, ", numberofPoint)
                    if numberofPoint>2:
                        objectId = self.poly(p['location'],fill=p['fill'])
                    elif numberofPoint==2 :
                        self.line(list_of_points)
                    else:
                        pass
                    self.drawn = objectId


    
    def deleted(self, event):
        temp = self.c.find_closest(event.x, event.y)[0]
        self.c.delete(temp)
       
    def copy(self, event):
        self.copy_data["item"] = self.c.find_closest(event.x, event.y)[0]
        self.copy_data["x"] = event.x
        self.copy_data["y"] = event.y
        
    def paste(self, event):
        findShape = self.c.type(self.copy_data["item"])
        paint_color = self.color
        
        if findShape == "oval":
            print("ok")
            objectId = self.oval(self.c.bbox(self.copy_data["item"]), fill=paint_color)
            self.drawn = objectId
        elif findShape == "rectangle":
            objectId = self.shape(self.c.bbox(self.copy_data["item"]), fill=paint_color)
            self.drawn = objectId
        elif findShape == "line":
            objectId = self.line(self.c.bbox(self.copy_data["item"]), fill=paint_color)
            self.drawn = objectId
        else: 
            objectId = self.poly(self.c.bbox(self.copy_data["item"]), fill=paint_color)
            self.drawn = objectId


    def groupDrag(self, event):
        # record the item and its location
        self.group_drag["item"] = self.c.find_closest(event.x, event.y)[0]
        self.group_drag["x"] = event.x
        self.group_drag["y"] = event.y

        print(self.group_drag)
        self.c.itemconfig(self.group_drag["item"], tag="NEW")
        print(self.c.itemcget(self.group_drag["item"], "tag"))
        
    def unGroup(self, event):
        # record the item and its location
        self.group_drag["item"] = self.c.find_closest(event.x, event.y)[0]
        self.group_drag["x"] = event.x
        self.group_drag["y"] = event.y

        print(self.group_drag)
        self.c.itemconfig(self.group_drag["item"], tag="OLD")
        print(self.c.itemcget(self.group_drag["item"], "tag"))
                
        
        
        
    def dragGroup(self, event):

        delta_x = event.x - self.group_drag["x"]
        delta_y = event.y - self.group_drag["y"]
        self.c.move("NEW", delta_x, delta_y)
        self.group_drag["x"] = event.x
        self.group_drag["y"] = event.y 
              
        
        
        

    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.c.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.c.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y 
              
    def onStart(self, event):
        self.start = event
        self.drawn = None       
    
    def onGrow(self, event):    
        paint_color = self.color                     
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = self.shape(self.start.x, self.start.y, event.x, event.y, fill=paint_color)
        self.drawn = objectId
        
    def onGrowPerfect(self, event):    
        paint_color = self.color                     
        canvas = event.widget
        diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
        signx = 1 if diffX >= 0 else -1
        signy = 1 if diffY >= 0 else -1
        if self.drawn: canvas.delete(self.drawn)
        size = max(abs(diffX), abs(diffY))
        objectId = self.shape(self.start.x, self.start.y, self.start.x+size*signx, self.start.y+size*signy, fill=paint_color)
        self.drawn = objectId

      
    def func_Draw_polygons(self,event):
        global mouse_xy
        mouse_xy= (event.x, event.y)
        paint_color = self.color 
        global poly, list_of_points
        center_x, center_y = mouse_xy
        self.c.delete(all)
    
        list_of_points.append((center_x, center_y))
    
        for pt in list_of_points:
            x, y =  pt
            #draw dot over position which is clicked
            x1, y1 = (center_x - 1), (center_y - 1)
            x2, y2 = (center_x + 1), (center_y + 1)
            self.oval(x1, y1, x2, y2, fill=paint_color, width=5)
    
        # add clicked positions to list
        numberofPoint=len(list_of_points)
        # Draw polygon
        if numberofPoint>2:
            poly=self.shape(list_of_points, fill=paint_color, outline=paint_color, width=2)
        elif numberofPoint==2 :
            self.line(list_of_points)
        else:
            pass
        print(list_of_points)
        
    def onClear(self, event):
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind('<Button 3>', self.reset)
        self.c.bind('<ButtonPress-1>', self.reset)  
        global list_of_points,poly, coord,Dict_Polygons,  mouse_xy
        coord=[]  # for saving coord of each click position
        Dict_Polygons={}   # Dictionary for saving polygons
        list_of_points=[]
        poly= None
        mouse_xy = None
        event.widget.delete('all')    
               
    def onMove(self, event):
        if self.drawn:                               
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            canvas.move(self.drawn, diffX, diffY)
            self.start = event
            
    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    coord=[]  # for saving coord of each click position
    
    Dict_Polygons={}   # Dictionary for saving polygons
    list_of_points=[]
    poly = None
    Paint()