from cgitb import text
from doctest import master
from tkinter.font import BOLD, ITALIC
from turtle import bgcolor
import customtkinter
import tkinter
from random import choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"
RIGHT_IMAGE = './images/check-circle-black.png'
WRONG_IMAGE = './images/x-circle-black.png'
DATA_FILE = './data/english_words.csv'
TO_LEARN = './data/words_to_learn.csv'
FONT_LANGUAGE = ("Courier", 40, ITALIC)
FONT_WORD = ("Courier", 60, BOLD)

current_word = {}


class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.title("FlashCard APP")

        customtkinter.set_appearance_mode('Dark')

        # ============ create two frames ============

        # configure grid layout (1x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=9, minsize=350)
        self.grid_rowconfigure(1, weight=1)

        self.frame_top = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_top.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        self.frame_top.rowconfigure(0, weight=1)
        self.frame_top.rowconfigure(1, weight=3, minsize=100)
        self.frame_top.columnconfigure(0, weight=1)
        self.frame_color = self.frame_top.bg_color

        self.frame_bottom = customtkinter.CTkFrame(master=self,
                                                   corner_radius=0)

        self.frame_bottom.grid(
            row=1, column=0, sticky="nswe", padx=20, pady=20)

        self.frame_bottom.rowconfigure(0, weight=1)
        self.frame_bottom.columnconfigure(1, weight=1, minsize=100)
        self.frame_bottom.columnconfigure(0, weight=1,minsize=100)

      
        self.label_language = customtkinter.CTkLabel(master=self.frame_top,
                                                     text="English",
                                                     text_font=FONT_LANGUAGE,
                                                     height=100,
                                                     corner_radius=6,
                                                     fg_color=(
                                                         "white", "gray38"),
                                                     justify=tkinter.LEFT)
        self.label_language.grid(
            column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.label_word = customtkinter.CTkLabel(master=self.frame_top,
                                                 text="",
                                                 text_font=FONT_WORD,
                                                 height=100,
                                                 corner_radius=6,
                                                 fg_color=("white", "gray38"),
                                                 justify=tkinter.LEFT)
        self.label_word.grid(column=0, row=1, sticky="nwe", padx=15, pady=15)

        img_wrong = tkinter.PhotoImage(file=WRONG_IMAGE)
        img_right = tkinter.PhotoImage(file=RIGHT_IMAGE)
        self.button_1 = customtkinter.CTkButton(master=self.frame_bottom,
                                                text="",
                                                image=img_right,
                                                command=self.known_word,
                                                fg_color=BACKGROUND_COLOR,
                                                hover_color = BACKGROUND_COLOR)
        self.button_1.grid(row=0, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_bottom,
                                                text="",
                                                image=img_wrong,
                                                command=self.next_word,
                                                bg_color=BACKGROUND_COLOR,
                                                fg_color=BACKGROUND_COLOR,
                                                hover_color = BACKGROUND_COLOR)
        self.button_2.grid(row=0, column=1, pady=10, padx=20)

    def next_word(self):
        global current_word
        self.after_cancel(self.flip_timer)
        current_word = choice(self.words_to_learn)
        self.label_word.configure(text=current_word['English'])
        self.frame_top.configure(fg_color=self.frame_color)
        self.frame_bottom.configure(fg_color=self.frame_color)
        self.config(bg=self.frame_color)
        self.label_language.configure(text="English")
        self.button_1.grid_forget()
        self.button_2.grid_forget()
        self.flip_timer = self.after(3000, self.flip_card)
        
        

    def flip_card(self):
        self.label_language.configure(text='Spanish')
        self.label_word.configure(text=current_word['Spanish'])
        self.frame_top.configure(fg_color=BACKGROUND_COLOR)
        self.frame_bottom.configure(fg_color=BACKGROUND_COLOR)
        self.config(bg=BACKGROUND_COLOR)
        self.button_1.grid(row=0, column=0, pady=10, padx=20)
        self.button_2.grid(row=0, column=1, pady=10, padx=20)



    def known_word(self):
        self.words_to_learn.remove(current_word)
        data = pandas.DataFrame(self.words_to_learn)
        data.to_csv(TO_LEARN, index=False)
        self.next_word()

    def read_file(self):
        try:
            words = pandas.read_csv(TO_LEARN)
        except FileNotFoundError:
            data_english = pandas.read_csv(DATA_FILE)
            self.words_to_learn = data_english.to_dict(orient="records")
        else:
            self.words_to_learn = words.to_dict(orient="records")


# ... program methods ...
if __name__ == "__main__":
    app = App()
    app.read_file()
    app.flip_timer = app.after(3000, app.flip_card)
    app.next_word()
    app.mainloop()
