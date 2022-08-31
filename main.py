# 'https://www.inventicons.com/inventicons'>Add Chart vector icon created by Invent Icons - InventIcons.com


from tkinter import DISABLED, font
import Kurve
from PIL import Image, ImageTk
import os
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter
import tkinter.messagebox
import customtkinter
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("green")
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
        self.minsize(800, 350)
        # call .on_closing() when app gets closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        image_size = 20
        self.curves_buttons = []
        self.sections_buttons = []
        self.curves = []
        self.zyklus = ""
        self.show_time = 0

        add_curve_image = ImageTk.PhotoImage(Image.open(
            PATH + "/images/add-curve.png").resize((image_size, image_size)))
        add_section_image = ImageTk.PhotoImage(Image.open(
            PATH + "/images/add-section.png").resize((image_size, image_size)))

        # ============ create tree frames ============

        # configure grid layout (3x2)
        self.grid_columnconfigure(1, weight=1, minsize=230, )
        self.grid_rowconfigure(0, weight=1, minsize=380)

        self.frame_left = customtkinter.CTkFrame(
            master=self, name="f_left", width=80, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_main = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_main.grid(row=0, column=1, sticky="nswe", padx=0, pady=0)

        self.frame_main.grid_columnconfigure(0, weight=1)
        self.frame_main.grid_rowconfigure(1, weight=1)

        self.frame_menu = customtkinter.CTkFrame(
            master=self.frame_main, height=30, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nswe",
                             padx=(20, 0), pady=0, columnspan=2)

        # configure grid layout for main (1x2)
        self.frame_middle = customtkinter.CTkFrame(master=self.frame_main)
        self.frame_middle.grid(
            row=1, column=0, sticky="nswe", padx=(20, 20), pady=(10, 0))

        self.frame_right = customtkinter.CTkFrame(
            master=self.frame_main, width=200)

        # ============ frame_left ============

        self.label_curve_name = customtkinter.CTkLabel(
            master=self.frame_left, text="Leer", text_font=("Roboto Medium", -16))
        self.label_curve_name.grid(row=0, column=0, pady=10, padx=10)

        self.button_new_section = customtkinter.CTkButton(
            master=self.frame_left, image=add_section_image, text="", width=50, command=self.button_new_section_click)
        self.button_new_section.grid(row=9, column=0, pady=10, padx=10)

        self.optionmenu_theme = customtkinter.CTkOptionMenu(master=self.frame_left, values=[
                                                            "Light", "Dark", "System"], command=self.change_appearance_mode)
        self.optionmenu_theme.grid(
            row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_menu ============

        self.button_new_curve = customtkinter.CTkButton(
            master=self.frame_menu, text="", image=add_curve_image, command=self.open_new_curve_window, width=70, height=30)
        self.button_new_curve.grid(row=0, column=100, pady=5, padx=10)

    def draw_frame_right_curve(self):
        for widget in self.frame_right.winfo_children():
            widget.destroy()

        self.label_frame_right = customtkinter.CTkLabel(
            master=self.frame_right, text="Daten "+self.active_curve.name, text_font=("Roboto Medium", -12))
        self.label_frame_right.grid(
            row=0, column=0, columnspan=1, pady=10, padx=0)

        self.entry_time = customtkinter.CTkEntry(master=self.frame_right, width=60)
        self.entry_time.bind("<Return>", self.show_data_at_time)
        if self.show_time != 0:
            self.entry_time.insert(0,self.show_time)
        else:
            self.entry_time.insert(0,0)
        self.entry_time.grid(row=1, column=0)
        

        self.label_p_at_t = customtkinter.CTkLabel(master=self.frame_right, text="p({})".format(self.show_time))
        self.label_p_at_t.grid(row=2, column=0)
        self.label_v_at_t = customtkinter.CTkLabel(master=self.frame_right, text="v({})".format(self.show_time))
        self.label_v_at_t.grid(row=3, column=0)
        self.label_a_at_t = customtkinter.CTkLabel(master=self.frame_right, text="a({})".format(self.show_time))
        self.label_a_at_t.grid(row=4, column=0)

        self.label_p_at_time = customtkinter.CTkLabel(master=self.frame_right, text="set_time")
        self.label_p_at_time.grid(row=2, column=1)
        self.label_v_at_time = customtkinter.CTkLabel(master=self.frame_right, text="set_time")
        self.label_v_at_time.grid(row=3, column=1)
        self.label_a_at_time = customtkinter.CTkLabel(master=self.frame_right, text="set_time")
        self.label_a_at_time.grid(row=4, column=1)

        self.entry_pos = customtkinter.CTkEntry(master=self.frame_right, width=60, placeholder_text="time")
        self.entry_pos.bind("<Return>", self.show_data_at_pos)
        self.entry_pos.grid(row=5, column=0)

        self.label_t_at_pos = customtkinter.CTkLabel(master=self.frame_right, text="t_at_pos")
        self.label_t_at_pos.grid(row=6, column=0)

        self.label_p_at_pos = customtkinter.CTkLabel(master=self.frame_right, text="set_pos")
        self.label_p_at_pos.grid(row=6, column=1)

        self.label_p_min = customtkinter.CTkLabel(master=self.frame_right, text="P min = "+str(self.active_curve.p_min))
        self.label_p_min.grid(row=7, column=0)
        self.label_p_max = customtkinter.CTkLabel(master=self.frame_right, text="P max = "+str(self.active_curve.p_max))
        self.label_p_max.grid(row=7, column=1)

        self.label_v_min = customtkinter.CTkLabel(master=self.frame_right, text="V min = "+str(self.active_curve.v_min))
        self.label_v_min.grid(row=8, column=0)
        self.label_v_max = customtkinter.CTkLabel(master=self.frame_right, text="V max = "+str(self.active_curve.v_max))
        self.label_v_max.grid(row=8, column=1)

        self.label_a_min = customtkinter.CTkLabel(master=self.frame_right, text="A min = "+str(self.active_curve.a_min))
        self.label_a_min.grid(row=9, column=0)
        self.label_a_max = customtkinter.CTkLabel(master=self.frame_right, text="A max = "+str(self.active_curve.a_max))
        self.label_a_max.grid(row=9, column=1)
        
        
        self.frame_section_info = customtkinter.CTkFrame(master=self.frame_right, corner_radius=0)
        self.frame_section_info.grid(row=10, column=0, columnspan=2)

        for sec in self.active_curve.sections:
            label = customtkinter.CTkLabel(master=self.frame_section_info, text=sec.info)
            if sec.rule == "poly 5 c":
                label.configure(fg='#f00')
            label.pack(anchor="w")

        self.frame_right.grid(
            row=1, column=1, sticky="nse", padx=0, pady=(10, 0))
        self.show_data_at_time()

    def draw_frame_right_section(self):

        for widget in self.frame_right.winfo_children():
            widget.destroy()

        self.label_frame_right = customtkinter.CTkLabel(
            master=self.frame_right, text="Neuer Abschnitt", text_font=("Roboto Medium", -12))
        self.label_frame_right.grid(
            row=0, column=0, columnspan=1, pady=10, padx=0)

        self.dropdown_rule = customtkinter.CTkOptionMenu(
            master=self.frame_right, values=["Rast", "v. const.", "Poly 5"])
        self.dropdown_rule.grid(row=0, column=1, columnspan=1, pady=0, padx=10)
        self.dropdown_rule.set("Bewegungsgesetz")
        # ============ frame_right_start ============
        self.frame_right_start = customtkinter.CTkFrame(
            master=self.frame_right, corner_radius=0)
        self.frame_right_start.grid(
            row=1, column=0, columnspan=2, pady=5, padx=2)

        self.label_t_start = customtkinter.CTkLabel(
            master=self.frame_right_start, text="t_start", text_font=("Roboto Medium", -10), width=60)
        self.label_t_start.pack(side="left")
        self.entry_t_start = customtkinter.CTkEntry(
            master=self.frame_right_start, width=60, placeholder_text="t_start")
        self.entry_t_start.pack(side="left")

        self.label_p_start = customtkinter.CTkLabel(
            master=self.frame_right_start, text="s_start", text_font=("Roboto Medium", -10), width=60)
        self.label_p_start.pack(side="left")
        self.entry_p_start = customtkinter.CTkEntry(
            master=self.frame_right_start, width=60, placeholder_text="s_start")
        self.entry_p_start.pack(side="left")
        # ============ frame_right_end ============
        self.frame_right_end = customtkinter.CTkFrame(
            master=self.frame_right, corner_radius=0)
        self.frame_right_end.grid(
            row=2, column=0, columnspan=2, pady=5, padx=2)

        self.label_t_end = customtkinter.CTkLabel(
            master=self.frame_right_end, text="t_end", text_font=("Roboto Medium", -10), width=60)
        self.label_t_end.pack(side="left")
        self.entry_t_end = customtkinter.CTkEntry(
            master=self.frame_right_end, width=60, placeholder_text="t_end")
        self.entry_t_end.pack(side="left")

        self.label_p_end = customtkinter.CTkLabel(
            master=self.frame_right_end, text="s_end", text_font=("Roboto Medium", -10), width=60)
        self.label_p_end.pack(side="left")
        self.entry_p_end = customtkinter.CTkEntry(
            master=self.frame_right_end, width=60, placeholder_text="s_end")
        self.entry_p_end.pack(side="left")
        # ============ frame_right buttons ============
        self.button_calculate = customtkinter.CTkButton(
            master=self.frame_right, text="Abschnitt erstellen", command=self.create_new_section)
        self.button_calculate.grid(row=11, column=1, pady=10, padx=20)

    def populate_existing_section_frame(self, this_section: Kurve.Section):
        self.label_frame_right.configure(
            text="Abschnitt {}".format(this_section.pos))
        self.dropdown_rule.set(this_section.rule)
        self.entry_t_start.insert(0, this_section.t_s)
        self.entry_p_start.insert(0, this_section.p_s)
        self.entry_t_end.insert(0, this_section.t_e)
        self.entry_p_end.insert(0, this_section.p_e)

        self.button_calculate.configure(
            text="Übernehmen", command=self.update_section)

    def populate_sucsessor_frame(self, previous_section: Kurve.Section):
        self.entry_t_start.insert(0, previous_section.t_s)
        self.entry_p_start.insert(0, previous_section.p_s)

    def create_new_curve_button(self):
        text = "Kurve {}".format(len(self.curves_buttons)+1)
        self.curves_buttons.append(customtkinter.CTkButton(master=self.frame_menu, text=text, command=lambda c=len(
            self.curves_buttons): self.button_existing_curve_click(c), width=70, height=30))

        self.curves_buttons[len(self.curves_buttons)-1].grid(row=0,
                                                             column=len(self.curves_buttons), pady=5, padx=5)

    def show_section_frame(self):
        try:
            existing_sections = len(self.active_curve.sections)
        except:
            print("initalising GUI")
            existing_sections = 0

        if existing_sections == 0:
            self.draw_frame_right_section()
        else:
            self.draw_frame_right_section()
            self.populate_sucsessor_frame(
                self.active_curve.sections[-1])
        self.frame_right.grid(
            row=1, column=1, sticky="nse", padx=0, pady=(10, 0))

    def button_existing_curve_click(self, c):
        self.curves_buttons[c].configure(fg_color="blue")
        # ['#72CF9F', '#11B384']
        for i, btns in enumerate(self.curves_buttons):
            if i != c:
                # hard code achtung besser machen (notfall farbe von anderem button übernehmen)
                self.curves_buttons[i].configure(
                    fg_color=['#72CF9F', '#11B384'])
        self.label_curve_name.configure(text=self.curves_buttons[c].text)
        self.set_active_curve(c)  # aktive Kurve festlegen
        self.graph()
        self.draw_frame_right_curve()
        self.section_buttons_display()

    def create_new_curve(self):
        self.motor = self.entry_motor.get()
        self.zyklus = self.entry_zyklus.get()
        self.name = self.entry_name.get()
        self.takt = self.entry_takt.get()
        self.new_curve_window.destroy()

        self.frame_right.grid_forget()
        self.create_new_curve_button()
        #======== display new button as curent curve button
        self.curves_buttons[-1].configure(fg_color="blue")
        # ['#72CF9F', '#11B384']
        for i, btns in enumerate(self.curves_buttons[:-1]):

            self.curves_buttons[i].configure(
                fg_color=['#72CF9F', '#11B384'])

        newcurve = Kurve.Curve(self.name, int(self.takt), int(self.zyklus))
        self.curves.append(newcurve)
        self.set_active_curve(len(self.curves)-1)

    def set_active_curve(self, curve_i):
        self.active_curve = self.curves[curve_i]

    def set_active_section(self, section_i):
        self.section_index = section_i
        self.active_section = self.active_curve.sections[section_i]

    def section_buttons_display(self):
        for widget in self.frame_left.winfo_children():
            if str(widget)[-4:-1] == "btn":
                widget.destroy()

        self.sections_buttons.clear()
        for i, sec in enumerate(self.active_curve.sections):
            self.sections_buttons.append(customtkinter.CTkButton(master=self.frame_left, name="btn{}".format(i+1), text="Abschnitt {}".format(i+1), command=lambda c_s=i: self.button_existing_section_click(c_s), width=70, height=30))
            if sec.rule == "poly 5 c":
                self.sections_buttons[i].configure(fg_color="red", state=DISABLED)
            self.sections_buttons[i].grid(row=i+1, column=0, pady=5, padx=5)

    def new_section_button(self):
        number = "{}".format(len(self.sections_buttons)+1)
        self.sections_buttons.append(customtkinter.CTkButton(master=self.frame_left, name="btn"+number,  text="Abschnitt "+number, command=lambda c_s=len(
            self.sections_buttons): self.button_existing_section_click(c_s), width=70, height=30))
        self.sections_buttons[len(self.sections_buttons)-1].grid(
            row=len(self.sections_buttons), column=0, pady=5, padx=5)

    def button_new_section_click(self):
        self.show_section_frame()
        for i, btns in enumerate(self.sections_buttons):
            self.sections_buttons[i].configure(
                fg_color=['#72CF9F', '#11B384'])

    def button_existing_section_click(self, c_s):
        self.sections_buttons[c_s].configure(fg_color="blue")
        # ['#72CF9F', '#11B384']
        for i, btns in enumerate(self.sections_buttons):
            if i != c_s:
                # hard code farbe achtung besser machen (notfall farbe von anderem button übernehmen)
                self.sections_buttons[i].configure(
                    fg_color=['#72CF9F', '#11B384'])
        self.draw_frame_right_section()
        self.populate_existing_section_frame(self.active_curve.sections[c_s])
        self.frame_right.grid(
            row=1, column=1, sticky="nse", padx=0, pady=(10, 0))
        self.set_active_section(c_s)

    def create_new_section(self) -> None:
        rule = self.dropdown_rule.get()
        if rule == "Bewegungsgesetz":
            tkinter.messagebox.showwarning(
                title="Warnung", message="Choose a rule, moron!")
            return

        t_start = float(self.entry_t_start.get())
        t_end = float(self.entry_t_end.get())
        p_start = float(self.entry_p_start.get())
        p_end = float(self.entry_p_end.get())

        new_position = self.active_curve.get_number_of_sections() + 1

        new_section = self.active_curve.create_section(
            t_start, t_end, p_start, p_end, new_position, rule)

        self.active_curve.add_section(new_section)

        self.change_input_posibilities(t_end, p_end)
        self.new_section_button()
        self.section_buttons_display()
        self.graph()

    def update_section(self):  # button change section click
        #t_start = float(self.entry_t_start.get())
        t_end = float(self.entry_t_end.get())
        #p_start = float(self.entry_s_start.get())
        p_end = float(self.entry_p_end.get())
        rule = self.dropdown_rule.get()

        sec = self.active_curve.sections[self.section_index]

        self.active_curve.update_section(sec, t_end, p_end, rule)
        self.graph()

    def graph(self):
        for widget in self.frame_middle.winfo_children():
            widget.destroy()

        t = self.active_curve.t
        p = self.active_curve.p
        v = self.active_curve.v
        a = self.active_curve.a
        points = self.active_curve.points

        points_t = [i[0] for i in points]
        points_p = [i[1] for i in points]

        figure = Figure(figsize=(10, 6), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self.frame_middle)
        NavigationToolbar2Tk(figure_canvas, self.frame_middle)

        ax1 = figure.add_subplot(311)
        ax1.plot(t, p)
        ax1.set_xticks(np.arange(0, 390, 30))
        ax1.xaxis.tick_top()
        ax1.legend("p")
        ax1.scatter(points_t, points_p)
        ax1.grid(visible=True)

        ax2 = figure.add_subplot(312, sharex=ax1)
        ax2.plot(t, v)
        ax2.tick_params("x", labelbottom=False)
        ax2.grid(visible=True)

        ax3 = figure.add_subplot(313, sharex=ax1)
        ax3.plot(t, a)
        ax3.grid(visible=True)
        ax3.set_xlim(0, 360)

        figure_canvas.get_tk_widget().pack()
    
    def show_data_at_time(self,*args):
        self.show_time = float(self.entry_time.get())
        index = np.where(self.active_curve.t == self.show_time)
        np.set_printoptions(suppress=True) ###debug nicht notwendig----------

        pat = round(self.active_curve.p[index[0][0]],3)
        vat = round(self.active_curve.v[index[0][0]],3)
        aat = round(self.active_curve.a[index[0][0]],3)

        self.label_p_at_t.configure(text="p({})".format(self.show_time))
        self.label_v_at_t.configure(text="v({})".format(self.show_time))
        self.label_a_at_t.configure(text="a({})".format(self.show_time))

        self.label_p_at_time.configure(text=pat)
        self.label_v_at_time.configure(text=vat)
        self.label_a_at_time.configure(text=aat)

    def show_data_at_pos(self, *args):
        position = float(self.entry_pos.get())
        intersect_times = ""
        for sec in self.active_curve.sections:
            
            if  min([sec.p_s,sec.p_e]) < position < max([sec.p_s,sec.p_e]):
                time = sec.find_intersection(position)
                intersect_times += " and "+ str(time)

        self.label_p_at_pos.configure(text=intersect_times)


    def change_input_posibilities(self, t_end, s_end):
        self.entry_t_start.configure(state=tkinter.NORMAL, text_color="green")
        self.entry_t_start.delete(0, tkinter.END)
        self.entry_t_start.insert(0, t_end)
        self.entry_t_start.configure(
            state=tkinter.DISABLED, text_color="green")
        self.entry_t_end.delete(0, tkinter.END)
        self.entry_p_start.configure(state=tkinter.NORMAL, text_color="green")
        self.entry_p_start.delete(0, tkinter.END)
        self.entry_p_start.insert(0, s_end)
        self.entry_p_start.configure(
            state=tkinter.DISABLED, text_color="green")
        self.entry_p_end.delete(0, tkinter.END)

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def open_new_curve_window(self):
        self.new_curve_window = tkinter.Toplevel()
        self.new_curve_window.geometry("400x580")
        self.new_curve_window.title("Neue Kurve erstellen")
        self.new_curve_window.minsize(350, 200)

        self.new_curve_window.grid_columnconfigure(0, weight=1, minsize=230, )
        self.new_curve_window.grid_rowconfigure(0, weight=1, minsize=380)

        frame_new = customtkinter.CTkFrame(
            master=self.new_curve_window, corner_radius=10)
        frame_new.grid(row=0, column=0, sticky="nswe", pady=20, padx=20)

        label_1 = customtkinter.CTkLabel(master=frame_new, text="Neue Kurve:")
        label_1.grid(row=0, column=0, columnspan=2,
                     sticky="nswe", pady=20, padx=20)

        label_name = customtkinter.CTkLabel(
            master=frame_new, text="Benennung:")
        label_name.grid(row=1, column=0, sticky="nswe", pady=2, padx=2)
        self.entry_name = customtkinter.CTkEntry(
            master=frame_new, placeholder_text="Modul ...")
        self.entry_name.grid(row=1, column=1, sticky="nswe", pady=2, padx=2)

        label_motor = customtkinter.CTkLabel(master=frame_new, text="Motor:")
        label_motor.grid(row=2, column=0, sticky="nswe", pady=2, padx=2)
        self.entry_motor = customtkinter.CTkEntry(
            master=frame_new, placeholder_text="Motor")
        self.entry_motor.grid(row=2, column=1, sticky="nswe", pady=2, padx=2)

        label_zyklus = customtkinter.CTkLabel(master=frame_new, text="Zyklus:")
        label_zyklus.grid(row=3, column=0, sticky="nswe", pady=2, padx=2)
        self.entry_zyklus = customtkinter.CTkEntry(
            master=frame_new, placeholder_text="°")
        self.entry_zyklus.grid(row=3, column=1, sticky="nswe", pady=2, padx=2)

        label_takt = customtkinter.CTkLabel(master=frame_new, text="Takt:")
        label_takt.grid(row=4, column=0, sticky="nswe", pady=2, padx=2)
        self.entry_takt = customtkinter.CTkEntry(
            master=frame_new, placeholder_text="Zyklen/Minute")
        self.entry_takt.grid(row=4, column=1, sticky="nswe", pady=2, padx=2)

        button_create_curve = customtkinter.CTkButton(
            master=frame_new, text="Erstellen", width=40, command=self.create_new_curve)
        button_create_curve.grid(row=6, column=0, columnspan=2, pady=50)

        """ if self.zyklus != "":
            self.entry_zyklus.insert(0,self.zyklus)
        if self.takt != "":
            self.entry_takt.insert(0,self.takt) """  # wieder verwenden wenn filling ausgeschaltet wird

        # filling for easier debuging

        self.entry_takt.insert(0, "60")
        self.entry_name.insert(0, "Modul Eingang")
        self.entry_zyklus.insert(0, "360")
        self.entry_motor.insert(0, "VPL - 3601A4B14")

    def on_closing(self, event=0):
        self.destroy()
        self.quit()


if __name__ == "__main__":
    main()
