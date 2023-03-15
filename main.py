import tkinter as tk
from tkinter import ttk
import time
import pyautogui
import numpy as np
import random
import math
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
from threading import Thread
import datetime
import requests
import json
import sys

class ExampleApp(tk.Tk):

    map_point_1 = (0, 0)
    map_point_2 = (0, 0)

    screen_point_1 = (0, 0)
    screen_point_2 = (0, 0)

    shooting_point = (0, 0)
    repairing_point = (0, 0)

    helath_limit_point = (0, 0)

    ship_center_point = (0, 0)

    attacking_color = "#000000"
    repairing_color = "#000000"

    no_attacking_color = "#000000"
    no_repairing_color = "#000000"

    ONLINE = False

    VERSION = 1

    API_URL = "http://127.0.0.1:8083/"

    last_move = datetime.datetime.now()

    #labels
    label_coords = None
    attacking_color_label = None
    repairing_color_label = None
    health_limit_color_label = None

    #canvas
    attacking_canva = None
    repairing_canva = None
    health_limit_canva = None

    minimap_position_1_txt = None
    minimap_position_2_txt = None
    game_screen_position_1_txt = None
    game_screen_position_2_txt = None
    shooting_position_txt = None
    shoting_color_txt = None
    repairing_position_txt = None
    repairing_color_txt = None
    health_bar_position_txt = None
    ship_center_position_txt = None

    minimap_position_1 = "0,0"
    minimap_position_2 = "0,0"
    game_screen_position_1 = "0,0"
    game_screen_position_2 = "0,0"
    shooting_position = "0,0"
    no_attacking_color = "#000000"
    repairing_position = "0,0"
    no_repairing_color = "#000000"
    health_bar_position = "0,0"
    ship_center_position = "0,0"



    def __init__(self):
        super().__init__()
        
        #update root with self
        
        self.title("chrome")
        
        # create three frames
        self.frame1 = tk.Frame(self, height=100, width=100)
        self.frame2 = tk.Frame(self, height=100, width=100)
        #self.frame3 = tk.Frame(self, bg="green", height=100, width=100)
        
        # add widgets to each frame

        self.title = tk.Label(self.frame1, text="TOS")
        self.title.config(fg="black")
        self.title.config(font=("Courier", 44))
        self.title.pack()

        # add a text label color red
        self.sub_title = tk.Label(self.frame1, text="By: NotCheat, Almirante, NotNode \n", fg="black")
        self.sub_title.pack()


        self.label_coords = tk.Label(self.frame1, text="X: 0 Y: 0 \n")
        self.label_coords.pack()

        # hr line separator
        self.hr = tk.Label(self.frame1, text="\n\n [SCREEN] \n", fg="black")
        self.hr.pack()

        self.minimap_position = tk.Label(self.frame1, text="MINIMAP POSITIONS \n", fg="black")
        self.minimap_position.pack()

        #text input
        self.minimap_position_1_txt = tk.Entry(self.frame1, width=20)
        self.minimap_position_1_txt.pack()


        self.minimap_position_2_txt = tk.Entry(self.frame1, width=20)
        self.minimap_position_2_txt.pack()


        self.game_screen_position = tk.Label(self.frame1, text="GAME SCREEN", fg="black")
        self.game_screen_position.pack()

        #text input
        self.game_screen_position_1_txt = tk.Entry(self.frame1, width=20)
        self.game_screen_position_1_txt.pack()

        self.game_screen_position_2_txt = tk.Entry(self.frame1, width=20)
        self.game_screen_position_2_txt.pack()



        self.shoting_position = tk.Label(self.frame1, text="SHOTING POSITION", fg="black")
        self.shoting_position.pack()


        #text input
        self.shooting_position_txt = tk.Entry(self.frame1, width=20)
        self.shooting_position_txt.pack()


        self.shoting_color = tk.Label(self.frame1, text="SHOTING COLOR", fg="black")
        self.shoting_color.pack()


        #text input
        self.shoting_color_txt = tk.Entry(self.frame1, width=20)
        self.shoting_color_txt.pack()

        self.repairing_position = tk.Label(self.frame1, text="REPAIRING POSITION", fg="black")
        self.repairing_position.pack()

        #text input
        self.repairing_position_txt = tk.Entry(self.frame1, width=20)
        self.repairing_position_txt.pack()


        self.repairing_color = tk.Label(self.frame1, text="REPAIRING COLOR", fg="black")
        self.repairing_color.pack()


        #text input
        self.repairing_color_txt = tk.Entry(self.frame1, width=20)
        self.repairing_color_txt.pack()

        self.health_bar_position = tk.Label(self.frame1, text="HEALTH BAR POSITION", fg="black")
        self.health_bar_position.pack()


        #text input
        self.health_bar_position_txt = tk.Entry(self.frame1, width=20)
        self.health_bar_position_txt.pack()




        self.ship_centered = tk.Label(self.frame1, text="CENTER POSITION", fg="black")
        self.ship_centered.pack()

        self.ship_center_position_txt = tk.Entry(self.frame1, width=20)
        self.ship_center_position_txt.pack()

        
        # ----------------- FRAME 2 -----------------


        #hr line separator
        self.hr = tk.Label(self.frame2, text="\n\n [COLORS]  \n\n", fg="black")
        self.hr.pack()

        #label
        self.attacking_color_label = tk.Label(self.frame2, text="ATTACKING #00000")
        self.attacking_color_label.pack()

        #canva with color
        self.attacking_canva = tk.Canvas(self.frame2, width=20, height=20, bg="black")
        self.attacking_canva.pack()

        #label
        self.repairing_color_label = tk.Label(self.frame2, text="REPAIRING #00000")
        self.repairing_color_label.pack()

        #canva with color
        self.repairing_canva = tk.Canvas(self.frame2, width=20, height=20, bg="black")
        self.repairing_canva.pack()

        #label
        self.health_limit_color_label = tk.Label(self.frame2, text="HEALTH LIMIT #00000")
        self.health_limit_color_label.pack()

        #canva with color
        self.health_limit_canva = tk.Canvas(self.frame2, width=20, height=20, bg="black")
        self.health_limit_canva.pack()

        # hr line separator
        self.hr = tk.Label(self.frame2, text="\n\n [GAME] \n\n", fg="black")
        self.hr.pack()


        #list dropdown
        self.combo = ttk.Combobox(
            self.frame2,
            state="readonly",
            values=["MAP 1 / X"]
        )
        self.combo.current(0)
        self.combo.pack()

  
        #label
        self.caution_5 = tk.Label(self.frame2, text="\n\n")
        self.caution_5.pack()

        #button play
        self.play = tk.Button(self.frame2, text="START BOTING", fg="black")
        self.play.pack()



        # add the frames to the window using grid
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)


        self.minimap_position_1_txt.insert(0, "1413,236")
        self.minimap_position_2_txt.insert(0, "1489,307")
        self.game_screen_position_1_txt.insert(0, "405,196")
        self.game_screen_position_2_txt.insert(0, "1523,912")
        self.shooting_position_txt.insert(0, "867,940")
        self.shoting_color_txt.insert(0, "#4b0706")
        self.repairing_position_txt.insert(0, "1076,940")
        self.repairing_color_txt.insert(0, "#262626")
        self.health_bar_position_txt.insert(0, "719,951")
        self.ship_center_position_txt.insert(0, "954,566")
        #self.username_txt.insert(0, "continente")
        #self.password_txt.insert(0, "epic0110")

        #update cords
        self.update_cords()
        #self.frame3.grid(row=0, column=2)

        #start bot when press start bot button
        self.play.config(command=self.start_bot)

    

    def start_bot(self):
        print("START BOT")

        self.minimap_position_1 = self.minimap_position_1_txt.get()
        self.minimap_position_2 = self.minimap_position_2_txt.get()
        self.game_screen_position_1 = self.game_screen_position_1_txt.get()
        self.game_screen_position_2 = self.game_screen_position_2_txt.get()
        self.shooting_position = self.shooting_position_txt.get()
        self.no_attacking_color = self.shoting_color_txt.get()
        self.repairing_position = self.repairing_position_txt.get()
        self.no_repairing_color = self.repairing_color_txt.get()
        self.health_bar_position = self.health_bar_position_txt.get()
        self.ship_center_position = self.ship_center_position_txt.get()

        #print in console all values
        print("MINIMAP POSITION 1: " + self.minimap_position_1)
        print("MINIMAP POSITION 2: " + self.minimap_position_2)
        print("GAME SCREEN POSITION 1: " + self.game_screen_position_1)
        print("GAME SCREEN POSITION 2: " + self.game_screen_position_2)
        print("SHOOTING POSITION: " + self.shooting_position)
        print("NO ATTACKING COLOR: " + self.no_attacking_color)
        print("REPAIRING POSITION: " + self.repairing_position)
        print("NO REPAIRING COLOR: " + self.no_repairing_color)
        print("HEALTH BAR POSITION: " + self.health_bar_position)
        print("SHIP CENTER POSITION: " + self.ship_center_position)
            

        #username = self.username_txt.get()
        #password = self.password_txt.get()
        #map = combo.get()
        

        #validate inputs
        if "," in self.minimap_position_1:
            minimap_position_1_arr = self.minimap_position_1.split(",")
            if minimap_position_1_arr[0].isnumeric() and minimap_position_1_arr[1].isnumeric():
                self.map_point_1 = (int(minimap_position_1_arr[0]), int(minimap_position_1_arr[1]))
            else:
                self.send_alert("ERROR", "minimap position not valid")
                return
        else:
            self.send_alert("ERROR", "minimap position not valid")
            return



        if "," in self.minimap_position_2:
            minimap_position_2_arr = self.minimap_position_2.split(",")

            if minimap_position_2_arr[0].isnumeric() and minimap_position_2_arr[1].isnumeric():
                self.map_point_2 = (int(minimap_position_2_arr[0]), int(minimap_position_2_arr[1]))
            else:
                self.send_alert("ERROR", "minimap position not valid")
                return
        else:
            self.send_alert("ERROR", "minimap position not valid")
            return


        if "," in self.game_screen_position_1:
            game_screen_position_1_arr = self.game_screen_position_1.split(",")
            if game_screen_position_1_arr[0].isnumeric() and game_screen_position_1_arr[1].isnumeric():
                self.screen_point_1 = (int(game_screen_position_1_arr[0]), int(game_screen_position_1_arr[1]))
            else:
                self.send_alert("ERROR", "game screen position not valid")
                return
        else:
            self.send_alert("ERROR", "game screen position not valid")
            return

        if "," in self.game_screen_position_2  :
            game_screen_position_2_arr = self.game_screen_position_2.split(",")
            if game_screen_position_2_arr[0].isnumeric() and game_screen_position_2_arr[1].isnumeric():
                self.screen_point_2 = (int(game_screen_position_2_arr[0]), int(game_screen_position_2_arr[1]))
            else:
                self.send_alert("ERROR", "game screen position not valid")
                return
        else:
            self.send_alert("ERROR", "game screen position not valid")
            return

        if "," in self.shooting_position:
            shooting_position_arr = self.shooting_position.split(",")
            if shooting_position_arr[0].isnumeric() and shooting_position_arr[1].isnumeric():
                self.shooting_point = (int(shooting_position_arr[0]), int(shooting_position_arr[1]))
            else:
                self.send_alert("ERROR", "shooting position not valid")
                return
        else:
            self.send_alert("ERROR", "shooting position not valid")
            return

        if "," in self.repairing_position:
            repairing_position_arr = self.repairing_position.split(",")
            if repairing_position_arr[0].isnumeric() and repairing_position_arr[1].isnumeric():
                self.repairing_point = (int(repairing_position_arr[0]), int(repairing_position_arr[1]))
            else:
                self.send_alert("ERROR", "repairing position not valid")
                return
        else:
            self.send_alert("ERROR", "repairing position not valid")
            return

        if "," in self.health_bar_position:
            health_bar_position_arr = self.health_bar_position.split(",")
            if health_bar_position_arr[0].isnumeric() and health_bar_position_arr[1].isnumeric():
                self.helath_limit_point = (int(health_bar_position_arr[0]), int(health_bar_position_arr[1]))
            else:
                self.send_alert("ERROR", "health bar position not valid")
                return

        if "," in self.ship_center_position:
            ship_center_position_arr = self.ship_center_position.split(",")
            if ship_center_position_arr[0].isnumeric() and ship_center_position_arr[1].isnumeric():
                self.ship_center = (int(ship_center_position_arr[0]), int(ship_center_position_arr[1]))
            else:
                self.send_alert("ERROR", "ship center position not valid")
                return
        else:
            self.send_alert("ERROR", "ship center position not valid")
            return
        
        '''
        #if username is empty
        if username == "":
            self.send_alert("ERROR", "username not valid")
            return

        #if password is empty
        if password == "":
            self.send_alert("ERROR", "password not valid")
            return

        '''

        #TODO add here server validation
        bot_thread = Thread(target=self.bot)
        bot_thread.start()
        


    def bot(self):
        print("BOT STARTED")
        
        if self.ONLINE == True:
            return
        
        model = YOLO('1x.pt')

        self.ONLINE = True
        
        while self.ONLINE:
            time.sleep(3) #REMOVE IN PRODUCTION...

            # TODO ADD REPAWN DETECTION
            # TODO ADD ATTACKING CLAN BASE DETECTION
            
            img = pyautogui.screenshot()
            npcs = model.predict(img)
            frame = np.array(img)
    
            print("BOTTING....")
    
    
            max_distance = 1000000
            smaller_distance = max_distance
            smaller_position = (0, 0)
            now = datetime.datetime.now()
    
            counter = 0
            
            for npc in npcs:
            
                annotator = Annotator(frame)
                boxes = npc.boxes
    
                for box in boxes:
                    counter += 1
                    b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
                    x = int((box.xyxy[0][0] + box.xyxy[0][2]) / 2)
                    y = int((box.xyxy[0][1] + box.xyxy[0][3]) / 2)
                    distance_to_user = np.sqrt((x - self.ship_center_point[0])**2 + (y - self.ship_center_point[1])**2) #DEFAULT CENTER
                    if distance_to_user < smaller_distance :
                        smaller_distance = distance_to_user
                        smaller_position = (x, y) 
    
            print("NPCS: ", counter)
            print("attack color: ", self.attacking_color)
            print("no attack color: ", self.no_attacking_color)

            if counter > 0 and self.attacking_color == self.no_attacking_color:
            
                #TODO detect low health      
                pyautogui.click(smaller_position[0], smaller_position[1])
                pyautogui.click(smaller_position[0], smaller_position[1])

                #sleep 2
                time.sleep(2)

                #drag random position in radius of 50
                pyautogui.dragTo(smaller_position[0] + random.randint(-50, 50), smaller_position[1] + random.randint(-50, 50), 0.5, button='left')
                pyautogui.click(smaller_position[0] + random.randint(-50, 50), smaller_position[1] + random.randint(-50, 50))

                pyautogui.press('f')  
                time.sleep(1)
                pyautogui.press('f')
                time.sleep(1)
                pyautogui.press('f')
            else:
                print("NO NPCS")   

                if (now - self.last_move).seconds > 30 and self.attacking_color == self.no_attacking_color:
                    self.last_move = now

                    p1 = self.map_point_1
                    p2 = self.map_point_1

                    # Find the minimum and maximum x and y values
                    min_x = min(p1[0], p2[0])
                    max_x = max(p1[0], p2[0])
                    min_y = min(p1[1], p2[1])
                    max_y = max(p1[1], p2[1])

                    # Generate a random x and y within the range
                    map_x = random.uniform(min_x, max_x)
                    map_y = random.uniform(min_y, max_y)

                    pyautogui.click(map_x, map_y)

                    pyautogui.dragTo(x=map_x+1, y=map_y+1, duration=0.5, button='left')


                    time.sleep(2)

                    angle = random.uniform(0, 2*math.pi)

                    movement_x =  1115 + 100*math.cos(angle)
                    movement_y = 588 + 100*math.sin(angle)

                    pyautogui.click(movement_x, movement_y)

                    time.sleep(1)
                    pyautogui.press('h')
        

    #update cords
    def update_cords(self):

        #print("updating cords")
        x, y = pyautogui.position()
        
        self.label_coords.config(text="X: " + str(x) + " Y: " + str(y))

        r,g,b = pyautogui.screenshot().getpixel(self.repairing_point)
        r_2,g_2,b_2 = pyautogui.screenshot().getpixel(self.shooting_point)
        r_3,g_3,b_3 = pyautogui.screenshot().getpixel(self.helath_limit_point)

        self.repairing_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        self.attacking_color = '#{:02x}{:02x}{:02x}'.format(r_2, g_2, b_2)
        self.health_color = '#{:02x}{:02x}{:02x}'.format(r_3, g_3, b_3)

        #set label
        self.attacking_color_label.config(text="ATTACKING: " + self.attacking_color)
        self.repairing_color_label.config(text="REPAIRING: " + self.repairing_color)
        self.health_limit_color_label.config(text="HEALTH: " + self.health_color)

        #set canva colors
        self.attacking_canva.config(bg=self.attacking_color)
        self.repairing_canva.config(bg=self.repairing_color)
        self.health_limit_canva.config(bg=self.health_color)

        self.after(100, self.update_cords)
    
    def send_alert(self, title, message):
        alert = tk.Tk()
        alert.title(title)
        alert.geometry("250x50")
        alert.wm_attributes("-topmost", 1)
        alert.resizable(0, 0)
        alert_text = tk.Label(alert, text=message)
        alert_text.pack()
        alert_button = tk.Button(alert, text="OK", fg="black", command=alert.destroy)
        alert_button.pack()
        alert.mainloop()

    def on_closing(self):
        print("CLOSING")
        self.ONLINE = False
        sys.exit(0)
        
if __name__ == '__main__':
    app = ExampleApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
