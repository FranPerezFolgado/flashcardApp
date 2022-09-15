from cgitb import text
from doctest import master
from tkinter.font import BOLD, ITALIC
from customtkinter import CTk, CTkButton, CTkFrame, CTkLabel
from tkinter import Canvas, PhotoImage
from random import choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FLASHCARD_IMAGE_FRONT = './images/card_front.png'
FLASHCARD_IMAGE_BACK = './images/card_back.png'
RIGHT_IMAGE = './images/check-circle.png'
WRONG_IMAGE = './images/x-circle.png'
DATA_FILE = './data/english_words.csv'
TO_LEARN = './data/words_to_learn.csv'

current_word = {}

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{530}x{550}")   
        self.title("Pomodoro APP")
        self.config(padx=50, pady=50)

        frame = CTkFrame(master=self,
                               width=400,
                               height=400,
                               corner_radius=10,
                               padx= 200,
                               pady= 100,
                               bg_color='white',
                               border_width=2)
        #frame.grid(row=0, column=0, sticky="nsew",columnspan=2)
        frame.pack(padx=20, pady=20)
        self.lbl_language = CTkLabel(master=frame, text ='English')
        self.lbl_language.grid(row=0, column=0)
        self.lbl_word = CTkLabel(master=frame, text ='')
        self.lbl_word.grid(row=1, column=0)
        #frame.config(width=400,height=400)

        ######################

        img_right = PhotoImage(file=RIGHT_IMAGE)
        btn_right = CTkButton(image=img_right, highlightthickness=0,
                           borderwidth=0, command=self.known_word, text='')
        btn_right.pack(padx=50, pady=100)

        img_wrong = PhotoImage(file=WRONG_IMAGE)
        btn_wrong = CTkButton(image=img_wrong, highlightthickness=0,
                           borderwidth=0, command=self.next_word, text='')
        btn_wrong.pack(padx=100, pady=100)

    def next_word(self):
        global current_word
        self.after_cancel(self.flip_timer)
        current_word = choice(self.words_to_learn)
        self.lbl_word.config(text=current_word['English'])
        '''   self.flashcard.itemconfigure(
            self.lbl_word, text=current_word['English'], fill='black')
        self.flashcard.itemconfig(self.lbl_language, text="English", fill='black')
        self.flashcard.itemconfig(self.flashcard_img, image=self.flashcard_front)'''
        
       


    def flip_card(self):
        self.lbl_language.config(text='Spanish')
        self.lbl_word.config(text=current_word['Spanish'])
        '''self.flashcard.itemconfig(self.flashcard_img, image=self.flashcard_back)
        self.flashcard.itemconfig(self.lbl_language, text="Spanish", fill='white')
        self.flashcard.itemconfig(self.lbl_word, text=current_word['Spanish'], fill='white')'''
        pass


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
