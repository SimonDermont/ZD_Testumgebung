import tkinter
import tkinter.messagebox
import customtkinter

def main():
    app = App()
    app.mainloop()

class App(customtkinter.CTk):

    WIDTH = 1000
    HEIGHT = 300

    def __init__(self):
        super().__init__()

        self.title("Zeitdiagramm")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")


if __name__ == "__main__":
    main()