from base2 import *
from PIL import Image, ImageTk
import base2
import threading




class ImageMap2(ImageMap):
    def __init__(self,master, size, **kwargs):
        super(ImageMap2,self).__init__(master, size, **kwargs)
        self.master=master
        arrow_img = Image.open("./images/子弹.png").resize((50,50))
        arrow_img1 = Image.open("./images/子弹1.png").resize((50,50))
        self.TM =AbstractGrid.get_image((50,50),"./images/女八路.png")
        self.arrow={}
        self.arrow["W"]=ImageTk.PhotoImage(arrow_img1.rotate(180))
        self.arrow["S"]=ImageTk.PhotoImage(arrow_img1)
        self.arrow["A"]=ImageTk.PhotoImage(arrow_img.rotate(180))
        self.arrow["D"]=ImageTk.PhotoImage(arrow_img)
    def draw_entity(self,position:Position,tile_type:Entity):
        if tile_type.display()==TIME_MACHINE:
            x, y = self.get_position_center(position)
            c=self.create_image(x,y, anchor=tk.CENTER,image=self.TM)
            self.lis.append(c)
        else :
            super().draw_entity(position,tile_type)
    def print(self,text_ls:list):
        x=self.width/2
        y=self.height
        tmps=[]
        move=5
        while(True):
            k=y
            for tmp in tmps:
                self.delete(tmp)
            for text in text_ls:
                if k>self.height:break
                tmp=self.create_text(x, k, text=text,font=self.font('newspaper',size=15,weight_=2))
                tmps.append(tmp)
                self.master.update()
                k+=25
            time.sleep(0.1)
            if k<self.height/6*5:
                time.sleep(5)
                for tmp in tmps:
                    self.delete(tmp)
                break
            y-=move



class MastersGraphicalInterface(ImageGraphicalInterface):
    def __init__(self,root:tk.Tk,size):
        super(MastersGraphicalInterface,self).__init__(root,size)
        self.music=music
        self.bgs=[]
        self.bgs.append(AbstractGrid.get_image((self.bm.width+50,self.bm.height+50),path="./images/大渡河.png"))
        self.bgs.append(AbstractGrid.get_image((self.bm.width+50,self.bm.height+50),path="./images/铁索.png"))
        self.bgs.append(AbstractGrid.get_image((self.bm.width+50,self.bm.height+50),path="./images/草地.png"))
        self.bgs.append(AbstractGrid.get_image((self.bm.width+50,self.bm.height+50),path="./images/雪山.png"))
        self.bm = ImageMap2(root, size)
        self.bm.grid(row=1, column=0)
        self.bm.draw_bg()
        self.music.cycle += 1
        self.music.play("开场1",-1)
        text1="红军第五次反围剿在王明。的“左倾”错误指导下失败。被迫长征。  " \
              "历史意义：完成了战略转移。历经曲折，战胜了重重艰难险阻。" \
              "保存和锻炼了革命的基干力量。宣传了党的宗旨。" \
              "发扬了革命集体主义。革命英雄主义。革命乐观主义。" \
              "为开展抗日战争。和发展中国革命事业创造了条件。"
        self.bm.print(text1.split("。"))
        self.music.play("开场2",-1)
        text1="长征是艰难的，胜利是不易的。" \
              "在长征的路途上，请捡起武器。" \
              "在长征的路途上，请捡起药瓶。" \
              "在长征的路途上，请带上战友。" \
              "在抵达延安前。" \
              "对于一切反动势力，请消灭他们。" \
              "对于一切反动势力，请消灭他们。" \
              "对于一切反动势力，请消灭他们。" \
              "这将是你的通关条件。" \
              "加油，后浪。"
        self.bm.print(text1.split("。"))
        self.backgames=[None,None,None,None,None]
        self.index=0
        self.init=True
        self.change_bg = False
    def saveBackfive(self,game):
        self.backgames[self.index]=(game._player_position,game._grid._tiles.copy())
        self.index+=1
        self.index=self.index%5
    def get_back(self,game):
        if game.get_steps()<=5:
            return self.backgames[0]
        else:
            return self.backgames[self.index]
    def _move(self, game, direction):
        offset = game.direction_to_offset(direction)
        if offset is not None:
            game.move_player(offset=offset)
            for position, entity in game._grid.get_mapping().items():
                if entity.display() == PLAYER:
                    entity.step(position, game)
                    game._steps+=1
        self.saveBackfive(game)
        position=Position(7, 7)
        if game._steps % 5 == 0:
            entitys=game.get_grid().get_entities()
            flag=1
            for entity in entitys:
                if entity.display()==TRACKING_ZOMBIE:
                    flag=0
            if flag:
                p=TrackingZombie()
            else:
                p=Zombie()
            if position not in game._grid._tiles:
                game._grid._tiles[position]=p
        if game._steps % 10 == 0:
            self.change_bg=True
    def _step(self,game):
        self.music.zhandou_next()
        if self.change_bg:
            self.bm.draw_bg(self.bgs[game._steps // 10%4])
            self.change_bg=False
        if base2.PLAY:
            self.draw(game)
        if base2.PLAY and game.has_won():
            print("game.has_won")
            self.save_scores()
            base2.PLAY = False
            self.music.play("失败", -1)
        elif base2.PLAY and game.has_lost():
            print("game.has_lost")
            inventory=game.get_player().get_inventory()
            if inventory.contains(TIME_MACHINE):
                back=self.get_back(game)
                game._player_position=back[0]
                game._grid._tiles=back[1]
                tpos=None
                for pos in game._grid._tiles:
                    if game._grid._tiles[pos].display()==TIME_MACHINE:
                        tpos=pos
                        break
                if tpos:del game._grid._tiles[tpos]
                items=inventory.get_items()
                new_items=[]
                for item in items:
                    if item.display()!=TIME_MACHINE:
                        new_items.append(item)
                inventory._items=new_items
                game.get_player()._infected=False
            else:
                base2.PLAY=False
                self.music.play("失败",-1)
                self.lost_message()
        self.root.after(100, self._step,game)
    def zom_move(self,game):
        for position, entity in game._grid.get_mapping().items():
            if entity.display() in ZOMBIES:
                entity.step(position, game)
        self.root.after(1000, self.zom_move, game)
    def play(self, game):
        self.latst_key_time=0
        def key_thred(event):
            if self.init:
                base2.PLAY=True
                self.init=False
                self.music.zhandou_next()
            if time.time()-self.latst_key_time>=0.2 and PLAY:
                self.latst_key_time=time.time()
                t=threading.Thread(target=key_callback,args=((event,)))
                t.setDaemon(True)
                t.start()
        def key_callback(event):
            Fire_Dict={38:"W",40:"S",37:"A",39:"D"}
            if event.char in ["w", "a", "s", "d"] and PLAY:
                if event.char=="a":
                    self.bm.hero=self.bm.hero1
                elif event.char=="d":
                    self.bm.hero = self.bm.hero2
                self._move(game, event.char.capitalize())
            elif event.keycode in Fire_Dict and PLAY:
                Direction=Fire_Dict[event.keycode]
                fire(Direction)
        def fire(Direction):
            inventory = game.get_player().get_inventory()
            crow = inventory.get(CROSSBOW)
            if crow and crow.get_lifetime() > 0:
                crow.hold()
                start = game.get_grid().find_player()
                offset = game.direction_to_offset(Direction)
                if start is None or offset is None:
                    return  # Should never happen.

                grid = game.get_grid()
                position = start.add(offset)
                arrow = None
                while grid.in_bounds(position):
                    start_time=time.time()
                    while time.time()-start_time<0.3:
                        entity = grid.get_entity(position)
                        if entity is not None and entity.display() in ZOMBIES:
                            grid.remove_entity(position)
                            break
                        time.sleep(0.05)
                    else:
                        x, y = self.bm.get_position_center(position)
                        if arrow:
                            self.bm.delete(arrow)
                        arrow = self.bm.create_image(x, y, image=self.bm.arrow[Direction])
                        self.root.update()
                    position = position.add(offset)
                if arrow:
                    self.bm.delete(arrow)
        def Tfire(Direction):
            t = threading.Thread(target=fire, args=((Direction,)))
            t.setDaemon(True)
            t.start()
        def click_callback(event):
            if time.time() - self.latst_key_time >= 0.2 and PLAY:
                self.latst_key_time = time.time()
                pos=self.bm.pixel_to_position((event.x,event.y))
                if self.bm.inbounds(pos):
                    px=game._player_position.get_x()
                    py=game._player_position.get_y()
                    dx=pos.get_x()-px
                    dy=pos.get_y()-py
                    if math.fabs(dx)>=math.fabs(dy):
                        if dx>0:
                            Tfire("D")
                        elif dx<0:
                            Tfire("A")
                    else:
                        if dy>0:
                            Tfire("S")
                        elif dy<0:
                            Tfire("W")
        self.sb.set_info(game)
        self._step(game)
        self.zom_move(game)
        self.root.bind('<KeyPress>', key_thred)
        self.bm.bind('<ButtonRelease-1>', click_callback)
        base2.PLAY=False
        self.root.mainloop()


def main() -> None:
    """Entry point to gameplay."""
    game = great_game("maps/basic5.txt")
    root = tk.Tk()
    root.title('血色长征路')
    gui = MastersGraphicalInterface
    app = gui(root, game.get_grid().get_size())
    app.play(game)
if __name__ == '__main__':
    main()
