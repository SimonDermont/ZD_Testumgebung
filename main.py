
import tkinter
import tkinter.messagebox
import customtkinter
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

import Kurve

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = int(1920*0.8)
    HEIGHT = 500


    def __init__(self):
        super().__init__()

        self.title("Test1.py")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create tree frames ============

        # configure grid layout (3x1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_middle = customtkinter.CTkFrame(master=self)
        self.frame_middle.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=2, sticky="nse", padx=0, pady=0)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Kurve 1", text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left, text="Kurve erstellen", command=self.create_curve)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left, text="Button 2")
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left, text="Button 3")
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (2x9)
        self.frame_middle.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_middle.rowconfigure(9, weight=10)
        self.frame_middle.columnconfigure((0, 1), weight=1)
        self.frame_middle.columnconfigure(1, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_middle)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)


        # ============ frame_middle ============


        self.entry = customtkinter.CTkEntry(master=self.frame_middle, width=120, placeholder_text="CTkEntry")
        self.entry.grid(row=9, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_middle, text="print(len(self.curve.sections))", border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.debug_button)
                                                
        self.button_5.grid(row=9, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.optionmenu_1.set("Dark")
        self.button_3.configure(state="disabled", text="Disabled Button 3")

        # ============ frame_right ============
        self.frame_right.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_right.grid_rowconfigure(5, weight=0)  # empty row as spacing
        self.frame_right.grid_rowconfigure(8, minsize=10)    # empty row with minsize as spacing
        self.frame_right.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
        
        self.label_section1 = customtkinter.CTkLabel(master=self.frame_right, text="Section 1",text_font=("Roboto Medium", -12))
        self.label_section1.grid(row=0, column=0, columnspan=1, pady=2, padx=10)

        self.label_t_start = customtkinter.CTkLabel(master=self.frame_right, text="t_start",text_font=("Roboto Medium", -10))
        self.label_t_start.grid(row=1, column=0, columnspan=1, pady=2, padx=10)
        self.entry_t_start = customtkinter.CTkEntry(master=self.frame_right, width=60, placeholder_text="t_start" )
        self.entry_t_start.grid(row=1, column=1, pady=0, padx=20, columnspan=1)

        self.label_t_end = customtkinter.CTkLabel(master=self.frame_right, text="t_end",text_font=("Roboto Medium", -10))
        self.label_t_end.grid(row=2, column=0, columnspan=1, pady=2, padx=10,)
        self.entry_t_end = customtkinter.CTkEntry(master=self.frame_right, width=60, placeholder_text="t_end")
        self.entry_t_end.grid(row=2, column=1, pady=0, padx=20, columnspan=1)

        self.label_s_start = customtkinter.CTkLabel(master=self.frame_right, text="s_start",text_font=("Roboto Medium", -10))
        self.label_s_start.grid(row=3, column=0, columnspan=1, pady=2, padx=10)
        self.entry_s_start = customtkinter.CTkEntry(master=self.frame_right, width=60, placeholder_text="s_start")
        self.entry_s_start.grid(row=3, column=1, pady=0, padx=20, columnspan=1)

        self.label_s_end = customtkinter.CTkLabel(master=self.frame_right, text="s_end",text_font=("Roboto Medium", -10))
        self.label_s_end.grid(row=4, column=0, columnspan=1, pady=2, padx=10)
        self.entry_s_end = customtkinter.CTkEntry(master=self.frame_right, width=60, placeholder_text="s_end")
        self.entry_s_end.grid(row=4, column=1, pady=0, padx=20, columnspan=1)

        self.dropdown_rule = customtkinter.CTkOptionMenu(master=self.frame_right,values=["Rast", "v. const.", "Poly 5"])
        self.dropdown_rule.grid(row=5, column=1, pady=0, padx=20, columnspan=1)
        self.dropdown_rule.set("Bewegungsgesetz")

        self.button_calculate = customtkinter.CTkButton(master=self.frame_right, text="Abschnitt erstellen",command=self.create_section)
        self.button_calculate.grid(row=11,column=2, pady=10,padx=20)

        self.button_plot = customtkinter.CTkButton(master=self.frame_right, text="Kurve darstellen",command=self.graph)
        self.button_plot.grid(row=12,column=2, pady=10,padx=20)

    def create_curve(self):
        self.curve = Kurve.Curve("Kurve 1",60,360) #hard code 60, 360
        self.button_1.configure(state="disabled", text="Kurve 1")

    def create_section(self):
    
        t_start = float(self.entry_t_start.get())
        t_end = float(self.entry_t_end.get())
        s_start = float(self.entry_s_start.get())
        s_end = float(self.entry_s_end.get())
        rule = self.dropdown_rule.get()

        self.new_position = self.curve.get_number_of_sections() + 1

        self.sec = self.curve.create_section(t_start, t_end, s_start, s_end, self.new_position ,rule)

        self.curve.add_section(self.sec)
        self.show_sec_info()

        self.change_input_posibilities(t_end, s_end)

    def show_sec_info(self): #display sec info perma
        this_text = self.sec.info
        self.label = customtkinter.CTkLabel(master=self.frame_right, text=this_text)
        this_row = self.sec.pos+13
        self.label.grid(row=this_row,column=1)
 
    def graph(self): 
        
        t = self.curve.t
        p = self.curve.p
        v = self.curve.v
        a = self.curve.a
        points = self.curve.points

        points_t = [i[0] for i in points]
        points_p = [i[1] for i in points]

        ax1 = plt.subplot(311)
        plt.plot(t, p)
        plt.scatter(points_t,points_p)
        plt.tick_params('x', labelsize=6)
        plt.xticks(np.arange(0, 360, 30))
        ax1.legend("p")

        ax2 = plt.subplot(312, sharex=ax1)
        plt.plot(t, v)
        plt.tick_params('x', labelbottom=False)

        # share x and y
        ax3 = plt.subplot(313, sharex=ax1)
        plt.plot(t, a)
        plt.xlim(0, 360)
        plt.show()


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

    def debug_button(self):
        print(len(self.curve.sections))

    def on_closing(self, event=0):
        self.destroy()
        self.quit()

if __name__ == "__main__":
    app = App()
    app.mainloop()