from base1 import *
from tkinter import filedialog
import time
import pickle
import os
from PIL import Image, ImageTk
PLAY=True
music=Music()
class StatusBar(tk.Frame):
    def __init__(self,master,width,height,**kwargs):
        super(StatusBar,self).__init__(master=master,width=width,height=height,borderwidth=0,**kwargs)
        self.master=master
        self.width=width
        self.height=height
        self.width_each=width/5
        for i in range(5):
            self.columnconfigure(i, minsize=self.width_each)
        self.chasee = AbstractGrid.get_image((90,90),path="./images/黑白俩八路.png")
        self.yanan = AbstractGrid.get_image((120,120),path="./images/延安2.png")
        self.t1=tk.Canvas(self,height=self.height,width=self.width_each)
        self.t1.create_image(70,40,image=self.yanan,anchor=tk.CENTER)
        self.t1.grid(row=0, column=4)
        self.t2 = tk.Canvas(self, height=self.height, width=self.width_each)
        self.t2.create_image(60,40,image=self.chasee,anchor=tk.CENTER)
        self.t2.grid(row=0, column=0)
        self.Timer=AbstractGrid(self,rows=5,cols=1,width=self.width_each,height=self.height)
        self.Timer.grid(row=0,column=1)
        self.Moves=AbstractGrid(self,rows=5,cols=1,width=self.width_each,height=self.height)
        self.Moves.grid(row=0,column=2)
        self.bframe=tk.Frame(self,height=self.height,width=self.width_each)
        self.bframe.grid(row=0,column=3)
        self.Restart=tk.Button(self.bframe, text="重新开始",font=AbstractGrid.font(size=12),bd=0,command=self.restart_game)
        self.Quit=tk.Button(self.bframe, text="退出游戏",font=AbstractGrid.font(size=12),bd=0,command=self.quit_game)
        self.Restart.grid(row=1,column=0)
        self.Quit.grid(row=3,column=0)
        self.start_time=self.get_time()
    def draw(self,game):
        self.Timer.delete("all")
        self.Moves.delete("all")
        self.Timer.annotate_position(Position(0,1),text="时间".format(0,0),font=AbstractGrid.font(size=12))
        t=self.get_time()-self.start_time
        self.Timer.annotate_position(Position(0,3),text="{} 分 {} 秒".format(t//60,t%60),font=AbstractGrid.font(size=12))
        self.Moves.annotate_position(Position(0,1),text="移动".format(0,0),font=AbstractGrid.font(size=12))
        self.Moves.annotate_position(Position(0,3),text="{} 步".format(game.get_steps()),font=AbstractGrid.font(size=12))
    def restart_game(self):
        global PLAY
        self.start_time=self.get_time()
        loader = GreatMapLoader()
        grid = loader.load(MAP_FILE)
        self.game.__init__(grid)
        PLAY = True
        self.master.update()
        music.cycle=0
    def quit_game(self):
        self.quit()
    def set_info(self,game):
        self.game=game
    def save_game(self):
        path = filedialog.asksaveasfilename()
        data={"game":self.game,"time":self.get_time()-self.start_time}
        with open(path,"wb") as f:
            pickle.dump(data,f)
            f.close()
    def load_game(self):
        path=filedialog.askopenfilename()
        with open(path,"rb") as f:
            data=pickle.load(f)
            self.start_time=self.get_time()-data['time']
            game=data["game"]
            self.game._grid=game._grid
            self.game._steps=game._steps
            self.game._player_position=game._player_position
        music.cycle = 0
    def get_time(self):
        return int(time.time())
class ImageMap(BasicMap):
    def __init__(self,master, size, **kwargs):
        super(ImageMap,self).__init__(master, size, **kwargs)
        self.crossbow = self.get_image((50,50),"./images/gun.png")
        self.yaoping = self.get_image((50,50),"./images/药瓶.png")
        #self.hero = tk.PhotoImage(file=IMAGES[PLAYER])
        self.hero1 = self.get_image((50,50),"./images/男八路.png")
        self.hero2= self.get_image((50,50),"./images/男八路1.png")
        self.hero=self.hero1
        self.hospital = self.get_image((100,100),"./images/宝塔山.png")
        #self.hospital=tk.PhotoImage(file=IMAGES[HOSPITAL])
        self.fandongpai = self.get_image((50,50),"./images/反动派1.png")
        self.dafandongpai = self.get_image((70,70),"./images/大反派1.png")
        self.tile=tk.PhotoImage(file=IMAGES[BACK_GROUND])
        self.width=size * CELL_SIZE
        self.height = size * CELL_SIZE
        self.lis=[]
        self.bg=[]
    def draw_entity(self,position:Position,tile_type:Entity):
        x,y = self.get_position_center(position)
        if tile_type.display()==ZOMBIE:
            c=self.create_image(x,y, anchor=tk.CENTER,image=self.fandongpai)
        elif tile_type.display() ==TRACKING_ZOMBIE:
            c=self.create_image(x,y, anchor=tk.CENTER,image=self.dafandongpai)
        elif tile_type.display() ==GARLIC:
            c=self.create_image(x,y, anchor=tk.CENTER,image=self.yaoping)
        elif tile_type.display() ==CROSSBOW:
            c=self.create_image(x,y, anchor=tk.CENTER,image=self.crossbow)
        elif tile_type.display()==PLAYER:
            c=self.create_image(x,y, anchor=tk.CENTER,image=self.hero)
        elif tile_type.display()==HOSPITAL :
            c=self.create_image(x, y, anchor=tk.CENTER, image=self.hospital)
        else:
            return
        self.lis.append(c)
    def clear(self):
        for c in self.lis:
            self.delete(c)
        self.lis=[]
    def draw_bg(self,bg=None):
        tmps=[]
        if bg is None:
            for i in range(self.size):
                for j in range(self.size):
                    x, y = self.get_position_center(Position(i,j))
                    c=self.create_image(x, y,anchor=tk.CENTER, image=self.tile)
                    tmps.append(c)
        else:
            x, y = self.get_position_center(Position(4, 4))
            c=self.create_image(x, y, anchor=tk.CENTER, image=bg)
            tmps.append(c)
        for b in self.bg:
            self.delete(b)
        self.bg=tmps







class ImageGraphicalInterface:
    def __init__(self,root:tk.Tk,size):
        self.root=root
        self.root.iconphoto(False, tk.PhotoImage(file='./images/gun.png'))
        #self.root.geometry("{}x{}+{}+{}".format(size,size,size,size))
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.fullwidth=size*CELL_SIZE+INVENTORY_WIDTH
        self.headCanvas=AbstractGrid(master=root,rows=1,cols=1,height=CELL_SIZE*2,width=self.fullwidth)
        self.headCanvas.grid(row=0,column=0,columnspan=2)
        img=Image.open("./images/head.png")
        img=img.resize((self.fullwidth,CELL_SIZE*2),resample=Image.BICUBIC)
        self.banner_img=ImageTk.PhotoImage(img)
        self.headCanvas.create_image(0,0,anchor=tk.NW,image=self.banner_img)
        root.title("血色长征路")
        self.bm=ImageMap(root,size)
        self.iv=InventoryView(root,size)
        self.sb=StatusBar(root, height=80, width=self.fullwidth)
        self.bm.grid(row=1, column=0)
        self.iv.grid(row=1, column=1)
        self.sb.grid(row=2, column=0, columnspan=2)
        self.root.resizable(0, 0)
        self.Menu = tk.Menu(self.root)
        file = tk.Menu(self.Menu, tearoff=0)
        file.add_command(label="重新开始", command=self.sb.restart_game, font=AbstractGrid.font(size=12))
        file.add_command(label="存储游戏", command=self.sb.save_game, font=AbstractGrid.font(size=12))
        file.add_command(label="加载游戏", command=self.sb.load_game, font=AbstractGrid.font(size=12))
        file.add_command(label="高分榜", command=self.high_scores, font=AbstractGrid.font(size=12))
        file.add_command(label="退出", command=self.sb.quit_game, font=AbstractGrid.font(size=12))
        self.Menu.add_cascade(label="选项", menu=file, font=AbstractGrid.font(size=12))
        self.root.config(menu=self.Menu)
        def _sort(info):
            infos=info.split(",")
            return int(infos[-1])
        if os.path.exists(HIGH_SCORES_FILE):
            with open(HIGH_SCORES_FILE,"r") as f:
                fb=f.read()
                self.scores=fb.split("\n")
                while "" in self.scores:
                    self.scores.remove("")
                self.scores.sort(key=_sort)
                self.scores=self.scores[:3]
        else:
            self.scores=[]
    def high_scores(self):
        def _sort(info):
            infos=info.split(",")
            return int(infos[-1])
        if os.path.exists(HIGH_SCORES_FILE):
            with open(HIGH_SCORES_FILE,"r") as f:
                fb=f.read()
                self.scores=fb.split("\n")
                while "" in self.scores:
                    self.scores.remove("")
                self.scores.sort(key=_sort)
                self.scores=self.scores[:3]
        else:
            self.scores=[]
        def _quit_high_score():
            top.destroy()
        top = tk.Toplevel()
        top.resizable(0, 0)
        top.title('Top3')
        tophead=AbstractGrid(top,1,1,width=170,height=CELL_SIZE,bg=DARK_PURPLE)
        tophead.grid(row=0, column=0)
        tophead.annotate_position(Position(0,0),"High Scores",font=AbstractGrid.font(size=24),fill="white")
        topcanvas=AbstractGrid(top,len(self.scores) if len(self.scores) else 1,1,width=170,height=20*len(self.scores))
        topcanvas.grid(row=1, column=0)
        for i,info in enumerate(self.scores):
            infos=info.split(",")
            name=infos[0]
            t=int(infos[-1])
            m=t//60
            s=t%60
            if m:
                shows = "{}: {}m {}s".format(name,m,s)
            else:shows="{}: {}s".format(name,s)
            topcanvas.annotate_position(Position(0,i),shows,font=AbstractGrid.font(size=12))
        quit= tk.Button(top, text="Done", font=AbstractGrid.font(size=12), bd=0,
                                 command=_quit_high_score)
        quit.grid(row=2, column=0)

    def save_scores(self):
        score=self.sb.get_time()-self.sb.start_time
        def _enter():
            if os.path.exists(HIGH_SCORES_FILE):
                mode = "a"
            else:
                mode = "w"
            with open(HIGH_SCORES_FILE, mode) as f:
                f.write("{},{}\n".format(self.username.get(), score))
            top.destroy()
        def _enter_and_play():
            if os.path.exists(HIGH_SCORES_FILE):
                mode = "a"
            else:
                mode = "w"
            with open(HIGH_SCORES_FILE, mode) as f:
                f.write("{},{}\n".format(self.username.get(), score))
            top.destroy()
            self.sb.restart_game()
        m = score // 60
        s = score % 60
        top = tk.Toplevel()
        top.resizable(0, 0)
        top.title('革命成功!')
        label=tk.Label(top,anchor=tk.CENTER ,text="历时{}m,{}s! 请输入你的姓名:".format(m,s),font=AbstractGrid.font(size=12))
        label.grid(row=0, column=0,columnspan=2)
        self.username=tk.StringVar()
        namewidget= tk.Entry(top, width=30, font=AbstractGrid.font(size=12),
                                             textvariable=self.username )
        namewidget.grid(row=1, column=0,columnspan=2)
        enter= tk.Button(top, text="确认", font=AbstractGrid.font(size=12), bd=0,
                                 command=_enter)
        enter.grid(row=2, column=0)
        en_and_pla= tk.Button(top, text="重新开始", font=AbstractGrid.font(size=12), bd=0,
                                 command=_enter_and_play)
        en_and_pla.grid(row=2, column=1)
    def lost_message(self):
        top = tk.Toplevel()
        top.resizable(0, 0)
        top.title('革命失败!')
        def _enter():
            top.destroy()
        def _enter_and_play():
            top.destroy()
            self.sb.restart_game()

        top.rowconfigure(1, minsize=15)
        label=tk.Label(top,anchor=tk.CENTER ,text="长征是残酷的，在长征途中！",font=AbstractGrid.font(size=12))
        label.grid(row=0, column=0,columnspan=2)
        label=tk.Label(top,anchor=tk.CENTER ,text="红一方面军牺牲近八万人！",font=AbstractGrid.font(size=12))
        label.grid(row=1, column=0,columnspan=2)
        label=tk.Label(top,anchor=tk.CENTER ,text="红二方面军牺牲近一万人！",font=AbstractGrid.font(size=12))
        label.grid(row=2, column=0,columnspan=2)
        label=tk.Label(top,anchor=tk.CENTER ,text="红四方面军牺牲近七万人！",font=AbstractGrid.font(size=12))
        label.grid(row=3, column=0,columnspan=2)
        label=tk.Label(top,anchor=tk.CENTER ,text="革命还未胜利，同志仍需努力！",font=AbstractGrid.font(size=12))
        label.grid(row=4, column=0,columnspan=2)
        enter= tk.Button(top, text="确认", font=AbstractGrid.font(size=12), bd=0,
                                 command=_enter)
        enter.grid(row=5, column=0)
        en_and_pla= tk.Button(top, text="重新开始", font=AbstractGrid.font(size=12), bd=0,
                                 command=_enter_and_play)
        en_and_pla.grid(row=2, column=1)
    def _inventory_click(self, event, inventory):
        x = event.x
        y = event.y
        self.iv.toggle_item_activation((x,y),inventory)
    def draw(self, game:AdvancedGame):
        self.bm.clear()
        self.iv.delete("all")
        gm=game.get_grid().get_mapping()
        inventory = game.get_player().get_inventory()

        for position in gm:
            self.bm.draw_entity(position,gm[position])
        self.iv.draw(inventory)
        self.sb.draw(game)
    def _move(self, game, direction):
        offset = game.direction_to_offset(direction)
        if offset is not None:
            game.move_player(offset=offset)
            game.step()
    def _step(self,game):
        global PLAY
        if PLAY:
            self.draw(game)
        if PLAY and game.has_won():
            print("game.has_won")
            self.save_scores()
            PLAY = False
        elif PLAY and game.has_lost():
            print("game.has_lost")
            PLAY=False
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
        self.sb.set_info(game)
        self._step(game)
        self.root.bind('<KeyPress>', key_callback)
        self.iv.bind('<ButtonRelease-1>', click_callback)
        self.root.mainloop()
