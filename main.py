# 'https://www.inventicons.com/inventicons'>Add Chart vector icon created by Invent Icons - InventIcons.com

import tkinter
import tkinter.messagebox
import customtkinter
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


import os
from PIL import Image, ImageTk

import Kurve

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
PATH = os.path.dirname(os.path.realpath(__file__))

def main():
    app = App()
    app.mainloop()

class App(customtkinter.CTk):

    WIDTH = 1536
    HEIGHT = 500

    def __init__(self):
        super().__init__()

        self.title("Ein Traum aus Linien")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(800,350)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        image_size = 20
        self.curves_buttons = []
        self.sections_buttons = []
        self.curves = []
        self.zyklus = ""

        add_curve_image = ImageTk.PhotoImage(Image.open(PATH + "/images/add-curve.png").resize((image_size, image_size)))
        add_section_image = ImageTk.PhotoImage(Image.open(PATH + "/images/add-section.png").resize((image_size, image_size)))

        # ============ create tree frames ============

        # configure grid layout (3x2)
        self.grid_columnconfigure(1, weight=1, minsize=230, )
        self.grid_rowconfigure(0, weight=1, minsize=380)

        self.frame_left = customtkinter.CTkFrame(master=self, width=80, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_main = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_main.grid(row=0, column=1, sticky="nswe", padx=0, pady=0)

        self.frame_main.grid_columnconfigure(0, weight=1)
        self.frame_main.grid_rowconfigure(1, weight=1)

        self.frame_menu = customtkinter.CTkFrame(master=self.frame_main, height=30, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nswe", padx=(20,0), pady=0, columnspan=2)

        # configure grid layout for main (1x2)
        self.frame_middle = customtkinter.CTkFrame(master=self.frame_main)
        self.frame_middle.grid(row=1, column=0, sticky="nswe", padx=(20,20), pady=(10,0))

        self.frame_right = customtkinter.CTkFrame(master=self.frame_main, width=200)
        self.show_frame_right()


        # ============ frame_left ============

        self.label_curve_name = customtkinter.CTkLabel(master=self.frame_left, text = "Leer",text_font=("Roboto Medium", -16))
        self.label_curve_name.grid(row=0, column=0, pady=10, padx=10)

        self.button_show_section_frame = customtkinter.CTkButton(master=self.frame_left, image=add_section_image, text="", width=50, command=self.show_section_frame)
        self.button_show_section_frame.grid(row=9, column=0, pady=10, padx=10)

        self.optionmenu_theme = customtkinter.CTkOptionMenu(master=self.frame_left, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
        self.optionmenu_theme.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_menu ============

        self.button_new_curve = customtkinter.CTkButton(master=self.frame_menu, text="", image=add_curve_image, command=self.open_new_curve_window, width=70, height=30)
        self.button_new_curve.grid(row=0, column=100, pady=5, padx=10)
        
        # ============ frame_middle ============



        # ============ frame_right ============

        self.frame_right.grid_forget()

    def draw_frame_right(self):

        for widget in self.frame_right.winfo_children():
            widget.destroy()

        self.label_section1 = customtkinter.CTkLabel(master=self.frame_right, text="Section 1",text_font=("Roboto Medium", -12))
        self.label_section1.grid(row=0, column=0, columnspan=1, pady=10, padx=0)

        self.dropdown_rule = customtkinter.CTkOptionMenu(master=self.frame_right,values=["Rast", "v. const.", "Poly 5"])
        self.dropdown_rule.grid(row=0, column=1, columnspan=1, pady=0, padx=10)
        self.dropdown_rule.set("Bewegungsgesetz")
        # ============ frame_right_start ============
        self.frame_right_start = customtkinter.CTkFrame(master=self.frame_right, corner_radius=0)
        self.frame_right_start.grid(row=1, column=0, columnspan=2, pady=5, padx=2)

        self.label_t_start = customtkinter.CTkLabel(master=self.frame_right_start, text="t_start",text_font=("Roboto Medium", -10), width=60)
        self.label_t_start.pack(side="left")
        self.entry_t_start = customtkinter.CTkEntry(master=self.frame_right_start, width=60, placeholder_text="t_start" )
        self.entry_t_start.pack(side="left")

        self.label_s_start = customtkinter.CTkLabel(master=self.frame_right_start, text="s_start",text_font=("Roboto Medium", -10), width=60)
        self.label_s_start.pack(side="left")
        self.entry_s_start = customtkinter.CTkEntry(master=self.frame_right_start, width=60, placeholder_text="s_start")
        self.entry_s_start.pack(side="left")
        # ============ frame_right_end ============
        self.frame_right_end = customtkinter.CTkFrame(master=self.frame_right, corner_radius=0)
        self.frame_right_end.grid(row=2, column=0, columnspan=2, pady=5, padx=2)

        self.label_t_end = customtkinter.CTkLabel(master=self.frame_right_end, text="t_end",text_font=("Roboto Medium", -10), width=60)
        self.label_t_end.pack(side="left")
        self.entry_t_end = customtkinter.CTkEntry(master=self.frame_right_end, width=60, placeholder_text="t_end")
        self.entry_t_end.pack(side="left")

        self.label_s_end = customtkinter.CTkLabel(master=self.frame_right_end, text="s_end",text_font=("Roboto Medium", -10), width=60)
        self.label_s_end.pack(side="left")
        self.entry_s_end = customtkinter.CTkEntry(master=self.frame_right_end, width=60, placeholder_text="s_end")
        self.entry_s_end.pack(side="left")
        # ============ frame_right buttons ============
        self.button_calculate = customtkinter.CTkButton(master=self.frame_right, text="Abschnitt erstellen",command=self.create_new_section)
        self.button_calculate.grid(row=11,column=1, pady=10,padx=20)

        self.button_plot = customtkinter.CTkButton(master=self.frame_right, text="Kurve darstellen",command=self.graph)
        self.button_plot.grid(row=12,column=1, pady=10,padx=20)

    def draw_frame_right_existing(self):

        for widget in self.frame_right.winfo_children():
            widget.destroy()

        self.label_section1 = customtkinter.CTkLabel(master=self.frame_right, text="Section 1",text_font=("Roboto Medium", -12))
        self.label_section1.grid(row=0, column=0, columnspan=1, pady=10, padx=0)

        self.dropdown_rule = customtkinter.CTkOptionMenu(master=self.frame_right,values=["Rast", "v. const.", "Poly 5"])
        self.dropdown_rule.grid(row=0, column=1, columnspan=1, pady=0, padx=10)
        self.dropdown_rule.set("Bewegungsgesetz")
        # ============ frame_right_start ============
        self.frame_right_start = customtkinter.CTkFrame(master=self.frame_right, corner_radius=0)
        self.frame_right_start.grid(row=1, column=0, columnspan=2, pady=5, padx=2)

        self.label_t_start = customtkinter.CTkLabel(master=self.frame_right_start, text="t_start",text_font=("Roboto Medium", -10), width=60)
        self.label_t_start.pack(side="left")
        self.entry_t_start = customtkinter.CTkEntry(master=self.frame_right_start, width=60, placeholder_text="t_start" )
        self.entry_t_start.pack(side="left")

        self.label_s_start = customtkinter.CTkLabel(master=self.frame_right_start, text="s_start",text_font=("Roboto Medium", -10), width=60)
        self.label_s_start.pack(side="left")
        self.entry_s_start = customtkinter.CTkEntry(master=self.frame_right_start, width=60, placeholder_text="s_start")
        self.entry_s_start.pack(side="left")
        # ============ frame_right_end ============
        self.frame_right_end = customtkinter.CTkFrame(master=self.frame_right, corner_radius=0)
        self.frame_right_end.grid(row=2, column=0, columnspan=2, pady=5, padx=2)

        self.label_t_end = customtkinter.CTkLabel(master=self.frame_right_end, text="t_end",text_font=("Roboto Medium", -10), width=60)
        self.label_t_end.pack(side="left")
        self.entry_t_end = customtkinter.CTkEntry(master=self.frame_right_end, width=60, placeholder_text="t_end")
        self.entry_t_end.pack(side="left")

        self.label_s_end = customtkinter.CTkLabel(master=self.frame_right_end, text="s_end",text_font=("Roboto Medium", -10), width=60)
        self.label_s_end.pack(side="left")
        self.entry_s_end = customtkinter.CTkEntry(master=self.frame_right_end, width=60, placeholder_text="s_end")
        self.entry_s_end.pack(side="left")
        # ============ frame_right buttons ============
        self.button_calculate = customtkinter.CTkButton(master=self.frame_right, text="Änderung übernehmen",command=self.update_section)
        self.button_calculate.grid(row=11,column=1, pady=10,padx=20)     

    def new_curve_button(self):
        
        text = "Kurve {}".format(len(self.curves_buttons)+1)
        self.curves_buttons.append(customtkinter.CTkButton(master=self.frame_menu, text=text, command=lambda c=len(self.curves_buttons): self.button_existing_curve_click(c), width=70, height=30))
       
        self.curves_buttons[len(self.curves_buttons)-1].grid(row=0, column=len(self.curves_buttons), pady=5, padx=5)

    def show_frame_right(self):
        self.draw_frame_right()
        self.frame_right.grid(row=1, column=1, sticky="nse", padx=0, pady=(10,0))
    
    def button_existing_curve_click(self,c):
        self.curves_buttons[c].configure(fg_color="blue")
        #['#72CF9F', '#11B384']
        for i, btns in enumerate(self.curves_buttons):
            if i != c:
                self.curves_buttons[i].configure(fg_color=['#72CF9F', '#11B384']) # hard code achtung besser machen (notfall farbe von anderem button übernehmen)
        self.label_curve_name.configure(text=self.curves_buttons[c].text)
        self.active_curve(c) #aktive Kurve festlegen
        self.frame_right.grid_forget()

    def create_new_curve(self):

        self.motor = self.entry_motor.get()
        self.zyklus = self.entry_zyklus.get()
        self.name = self.entry_name.get()
        self.takt = self.entry_takt.get()
        self.new_curve_window.destroy()

        self.frame_right.grid_forget()
        self.new_curve_button()

        newcurve = Kurve.Curve(self.name ,int(self.takt), int(self.zyklus))
        self.curves.append(newcurve)
        self.active_curve(len(self.curves)-1)
        
    def active_curve(self,curve_i):
        self.curve_index = curve_i

    def active_section(self,section_i):
        self.section_index = section_i
        
    def show_section_frame(self):
        self.show_frame_right()
    
    def new_section_button(self):
        
        text = "Abschnitt {}".format(len(self.sections_buttons)+1)
        self.sections_buttons.append(customtkinter.CTkButton(master=self.frame_left, text=text, command=lambda c_s=len(self.sections_buttons): self.button_existing_section_click(c_s), width=70, height=30))
        self.sections_buttons[len(self.sections_buttons)-1].grid(row=len(self.sections_buttons), column=0, pady=5, padx=5)

    def button_existing_section_click(self,c_s):
        self.sections_buttons[c_s].configure(fg_color="blue")
        #['#72CF9F', '#11B384']
        for i, btns in enumerate(self.sections_buttons):
            if i != c_s:
                self.sections_buttons[i].configure(fg_color=['#72CF9F', '#11B384']) # hard code achtung besser machen (notfall farbe von anderem button übernehmen)
        self.draw_frame_right_existing()
        self.frame_right.grid(row=1, column=1, sticky="nse", padx=0, pady=(10,0))
        self.active_section(c_s)

    def create_new_section(self) -> None:
        t_start = float(self.entry_t_start.get())
        t_end = float(self.entry_t_end.get())
        s_start = float(self.entry_s_start.get())
        s_end = float(self.entry_s_end.get())
        rule = self.dropdown_rule.get()

        active_curve = self.curves[self.curve_index]

        self.new_position = active_curve.get_number_of_sections() + 1

        self.sec = active_curve.create_section(t_start, t_end, s_start, s_end, self.new_position ,rule)

        active_curve.add_section(self.sec)

        self.change_input_posibilities(t_end, s_end)
        self.new_section_button()
        self.graph()
    
    def update_section(self): #button change section click
        #t_start = float(self.entry_t_start.get())
        t_end = float(self.entry_t_end.get())
        #p_start = float(self.entry_s_start.get())
        p_end = float(self.entry_s_end.get())
        rule = self.dropdown_rule.get()

        active_curve = self.curves[self.curve_index]
        self.sec = active_curve.sections[self.section_index]

        active_curve.update_section(self.sec,t_end,p_end,rule)
        self.graph()
   
    def graph(self): 
        for widget in self.frame_middle.winfo_children():
            widget.destroy()
        active_curve = self.curves[self.curve_index]

        t = active_curve.t
        p = active_curve.p
        v = active_curve.v
        a = active_curve.a
        points = active_curve.points

        points_t = [i[0] for i in points]
        points_p = [i[1] for i in points]

        figure = Figure(figsize=(10,6),dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self.frame_middle)
        #NavigationToolbar2Tk(figure_canvas, self)


        ax1 = figure.add_subplot(311)
        ax1.plot(t,p)
        ax1.set_xticks(np.arange(0, 390, 30))
        ax1.xaxis.tick_top()
        ax1.legend("p")
        ax1.scatter(points_t,points_p)
        ax1.grid(visible=True)

        ax2 = figure.add_subplot(312, sharex=ax1)
        ax2.plot(t, v)
        ax2.tick_params("x", labelbottom=False)
        ax2.grid(visible=True)
        
        ax3 = figure.add_subplot(313, sharex=ax1)
        ax3.plot(t, a)
        ax3.grid(visible=True)
        ax3.set_xlim(0,360)
        
        figure_canvas.get_tk_widget().pack()
    
    def change_input_posibilities(self, t_end, s_end):
        self.entry_t_start.configure(state=tkinter.NORMAL, text_color="green")
        self.entry_t_start.delete(0, tkinter.END)
        self.entry_t_start.insert(0,t_end)
        self.entry_t_start.configure(state=tkinter.DISABLED, text_color="green")
        self.entry_t_end.delete(0, tkinter.END)
        self.entry_s_start.configure(state=tkinter.NORMAL, text_color="green")
        self.entry_s_start.delete(0, tkinter.END)
        self.entry_s_start.insert(0,s_end)
        self.entry_s_start.configure(state=tkinter.DISABLED, text_color="green")
        self.entry_s_end.delete(0, tkinter.END)

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def open_new_curve_window(self):
        self.new_curve_window = tkinter.Toplevel()
        self.new_curve_window.geometry("400x580")
        self.new_curve_window.title("Neue Kurve erstellen")
        self.new_curve_window.minsize(350,200)

        self.new_curve_window.grid_columnconfigure(0, weight=1, minsize=230, )
        self.new_curve_window.grid_rowconfigure(0, weight=1, minsize=380)

        frame_new = customtkinter.CTkFrame(master=self.new_curve_window, corner_radius=10)
        frame_new.grid(row=0, column=0, sticky="nswe", pady=20, padx=20)

        label_1 = customtkinter.CTkLabel(master=frame_new, text="Neue Kurve:")
        label_1.grid(row=0, column=0, columnspan=2, sticky="nswe", pady=20, padx=20)
        
        label_name = customtkinter.CTkLabel(master=frame_new, text="Benennung:")
        label_name.grid(row=1, column=0, sticky="nswe", pady=2, padx=2)
        self.entry_name =customtkinter.CTkEntry(master=frame_new,placeholder_text="Modul ...")
        self.entry_name.grid(row=1, column=1, sticky="nswe", pady=2, padx=2)

        label_motor = customtkinter.CTkLabel(master=frame_new, text="Motor:")
        label_motor.grid(row=2, column=0, sticky="nswe", pady=2, padx=2)
        self.entry_motor =customtkinter.CTkEntry(master=frame_new,placeholder_text="Motor")
        self.entry_motor.grid(row=2, column=1, sticky="nswe", pady=2, padx=2)

        label_zyklus = customtkinter.CTkLabel(master=frame_new, text="Zyklus:")
        label_zyklus.grid(row=3, column=0, sticky="nswe", pady=2, padx=2)
        self.entry_zyklus =customtkinter.CTkEntry(master=frame_new,placeholder_text="°")
        self.entry_zyklus.grid(row=3, column=1, sticky="nswe", pady=2, padx=2)

        label_takt = customtkinter.CTkLabel(master=frame_new, text="Takt:")
        label_takt.grid(row=4, column=0, sticky="nswe", pady=2, padx=2)
        self.entry_takt =customtkinter.CTkEntry(master=frame_new,placeholder_text="Zyklen/Minute")
        self.entry_takt.grid(row=4, column=1, sticky="nswe", pady=2, padx=2)

        button_create_curve = customtkinter.CTkButton(master = frame_new, text="Erstellen", width=40, command=self.create_new_curve)
        button_create_curve.grid(row=6, column=0, columnspan=2, pady=50)

        """ if self.zyklus != "":
            self.entry_zyklus.insert(0,self.zyklus)
        if self.takt != "":
            self.entry_takt.insert(0,self.takt) """ # wieder verwenden wenn filling ausgeschaltet wird

        #filling for easier debuging

        self.entry_takt.insert(0,"60")
        self.entry_name.insert(0,"Modul Eingang")
        self.entry_zyklus.insert(0,"360")
        self.entry_motor.insert(0,"VPL - 3601A4B14")


    def on_closing(self, event=0):
        self.destroy()
        self.quit()


if __name__ == "__main__":
    main()