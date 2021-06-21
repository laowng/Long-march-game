import tkinter as tk
from base0 import advanced_game
from constants import TASK, MAP_FILE
import math
import math
from base0 import *
import tkinter.font as tkFont
from PIL import Image,ImageTk
import pygame
class Music:
    def __init__(self):
        self.dict={"开场1":"./audios/zhandouqianxi.wav",
                   "开场2":"./audios/zhanchangxiaoyan.wav",
                   "战斗1":"./audios/zhandou.wav",
                   "战斗2":"./audios/zhongguojunhun.wav",
                   "胜利":"",
                   "失败":"./audios/zhanhuoqingshen.wav"}
        self.mixer=pygame.mixer
        self.mixer.init(channels=2)
        self.zhandou=["战斗2","战斗1"]
        self.cycle=0
    def play(self,name,*args,**kwargs):
        self.mixer.stop()
        self.mixer.music.load(self.dict[name])
        self.mixer.music.play(*args,**kwargs)
    def is_busy(self):
        return self.mixer.music.get_busy()
    def zhandou_next(self):
        if not self.is_busy() or self.cycle==0:
            self.play(self.zhandou[self.cycle%2],fade_ms=100)
            self.cycle += 1
class AbstractGrid(tk.Canvas):
    """
    a functional GUI-based version of EndOfDayz
    """
    def __init__(self, master, rows, cols, width, height, **kwargs):
        super(AbstractGrid,self).__init__(master, width=width, height=height, **kwargs)
        self.config(highlightthickness=0)
        self.rows=rows
        self.cols=cols
        self.row_each=height/self.rows
        self.col_each=width/self.cols
    @staticmethod
    def font(name="宋体", size=10, weight_=0):
        weight_ = ["normal", "roman", "bold", "italic"][weight_]
        return tkFont.Font(family=name, size=size, weight=weight_)

    @staticmethod
    def get_image(size,path):
        img=Image.open(path)
        img=img.resize(size,resample=Image.BICUBIC)
        return ImageTk.PhotoImage(img)
    def get_bbox(self, position):
        x_min=position.get_x()*self.col_each
        y_min=position.get_y()*self.row_each
        x_max=x_min + self.col_each
        y_max=y_min + self.row_each
        return (x_min,y_min,x_max,y_max)
    def inbounds(self,position):
        if position.get_y()<self.rows and position.get_x()<self.cols:
            return True
        else:
            return False
    def pixel_to_position(self, pixel):
        x=pixel[0]
        y=pixel[1]
        row=math.floor(y/self.row_each)
        col=math.floor(x/self.col_each)
        position=Position(col,row)
        return position
    def get_position_center(self, position):
        x_min, y_min, x_max, y_max=self.get_bbox(position)
        return (x_max+x_min)/2,(y_max+y_min)/2
    def annotate_position(self, position, text,**kwargs):
        x,y=self.get_position_center(position)
        self.create_text(x, y, text=text,**kwargs)

class BasicMap(AbstractGrid):
    def __init__(self,master, size, **kwargs):
        self.size=size
        super(BasicMap,self).__init__(master,rows=size, cols=size,bg="#808080", width=size*CELL_SIZE, height=size*CELL_SIZE, **kwargs)
    def draw_entity(self,position:Position,tile_type:Entity):
        color=None
        fc=None
        if tile_type.display()==ZOMBIE or tile_type.display()==TRACKING_ZOMBIE:
            color=LIGHT_GREEN
            fc = "black"
        elif tile_type.display() in PICKUP_ITEMS:
            color=LIGHT_PURPLE
            fc = "black"
        elif tile_type.display()==PLAYER or tile_type.display()==HOSPITAL:
            color=DARK_PURPLE
            fc="white"
        pos=self.get_bbox(position)
        self.create_rectangle(*pos,fill=color)
        self.annotate_position(position,tile_type.display(),fill=fc)

class InventoryView(AbstractGrid):
    def __init__(self, master, rows, **kwargs):
        super(InventoryView, self).__init__(master, rows=rows, cols=2,bg="#808080", width=INVENTORY_WIDTH, height=rows * CELL_SIZE, **kwargs)
        self.row_each=CELL_SIZE
        self.col_each=INVENTORY_WIDTH/2
        self.gun = self.get_image((45,45),"./images/gun.png")
        self.yaoping = self.get_image((45, 45), "./images/药瓶.png")
        self.TM =AbstractGrid.get_image((45,45),"./images/女八路.png")
    def draw(self, inventory:Inventory):
        pos0 = self.get_bbox(Position(0, 0))
        self.create_rectangle(0, pos0[1], self.col_each * 2, pos0[3], fill="#909090",width=0)
        self.create_text(self.col_each,self.row_each/2, text="背包",fill="white",font=self.font("宋体",size=25,weight_=2))
        self.pickups={}
        pks=inventory.get_items()
        for i,pk in enumerate(pks,1):
            name=pk.display()
            lt=pk.get_lifetime()
            fc = "black"
            x, y = self.get_position_center(Position(0,i))
            if pk.display()==CROSSBOW:
                self.create_image(x,y,anchor=tk.CENTER,image=self.gun)
            elif pk.display()==GARLIC:
                self.create_image(x,y,anchor=tk.CENTER,image=self.yaoping)
            elif pk.display()=="M":
                self.create_image(x,y,anchor=tk.CENTER,image=self.TM)
            else:
                self.annotate_position(Position(0,i),name,fill=fc,font=self.font(size=15))
            if pk.display()!="M":
                self.annotate_position(Position(1,i),lt,fill=fc,font=self.font(size=15))
            else:
                self.annotate_position(Position(1, i), "无限", fill=fc, font=self.font(size=15))
    def get_actived(self,inventory):
        pks = inventory.get_items()
        for i in range(len(pks)):
            if pks[i].is_active():
                return i,pks[i]
        return None,None
    def toggle_item_activation(self,pixel,inventory:Inventory):
        pass
class BasicGraphicalInterface:
    def __init__(self,root:tk.Tk,size):
        self.root=root
        #self.root.geometry("{}x{}+{}+{}".format(size,size,size,size))
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.headCanvas=AbstractGrid(master=root,rows=1,cols=1,height=CELL_SIZE,width=size*CELL_SIZE+INVENTORY_WIDTH,bg=DARK_PURPLE)
        x,y=self.headCanvas.get_position_center(Position(0,0))
        self.headCanvas.grid(row=0,column=0,columnspan=2)
        self.headCanvas.create_text(x,y,text=TITLE,font=AbstractGrid.font(size=20, weight_=2),fill="white")
        root.title("EndOfDayz")
        self.bm=BasicMap(root,size)
        self.iv=InventoryView(root,size)
        self.bm.grid(row=1, column=0)
        self.iv.grid(row=1, column=1)
        self.root.resizable(0, 0)
    def _inventory_click(self, event, inventory):
        x = event.x
        y = event.y
        self.iv.toggle_item_activation((x,y),inventory)
    def draw(self, game:AdvancedGame):
        self.bm.delete("all")
        self.iv.delete("all")
        gm=game.get_grid().get_mapping()
        inventory = game.get_player().get_inventory()
        for position in gm:
            self.bm.draw_entity(position,gm[position])
        self.iv.draw(inventory)
    def _move(self, game, direction):
        offset = game.direction_to_offset(direction)
        if offset is not None:
            game.move_player(offset=offset)
            game.step()
    def _step(self,game):
        self.draw(game)
        self.root.after(1000, self._step,game)
    def play(self, game):
        def key_callback(event):
            Fire_Dict={38:"W",40:"S",37:"A",39:"D"}
            if event.char in ["w", "a", "s", "d"]:
                self._move(game, event.char.capitalize())
                self._step(game)
            elif event.keycode in Fire_Dict:
                _, actived = self.iv.get_actived(game.get_player().get_inventory())
                if actived and actived.display() == CROSSBOW:
                    start = game.get_grid().find_player()
                    offset = game.direction_to_offset(Fire_Dict[event.keycode])
                    if start is None or offset is None:
                        return  # Should never happen.

                    # Find the first entity in the direction player fired.
                    first = first_in_direction(
                        game.get_grid(), start, offset
                    )

                    # If the entity is a zombie, kill it.
                    if first is not None and first[1].display() in ZOMBIES:
                        position, entity = first
                        game.get_grid().remove_entity(position)
                    else:
                        print(NO_ZOMBIE_MESSAGE)

        def click_callback(event):
            inventory=game.get_player().get_inventory()
            self._inventory_click(event,inventory)
        self._step(game)
        self.root.bind('<KeyPress>', key_callback)
        self.iv.bind('<ButtonRelease-1>', click_callback)
        self.root.mainloop()







