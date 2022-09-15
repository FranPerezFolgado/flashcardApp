from cProfile import label
from cgitb import text
from email.mime import image
from time import sleep
from tkinter import *
from tkinter.font import BOLD, ITALIC
import pandas
from random import choice
import time

BACKGROUND_COLOR = "#B1DDC6"
FLASHCARD_IMAGE_FRONT = './images/card_front.png'
FLASHCARD_IMAGE_BACK = './images/card_back.png'
RIGHT_IMAGE = './images/right.png'
WRONG_IMAGE = './images/wrong.png'
DATA_FILE = './data/english_words.csv'
TO_LEARN = './data/words_to_learn.csv'
words_to_learn = {}
current_word = {}


try:
    words = pandas.read_csv(TO_LEARN)
except FileNotFoundError:
    data_english = pandas.read_csv(DATA_FILE)
    words_to_learn = data_english.to_dict(orient="records")
else:
    words_to_learn = words.to_dict(orient="records")


def next_word():
    global current_word, flip_timer
    root.after_cancel(flip_timer)
    current_word = choice(words_to_learn)
    flashcard.itemconfigure(
        lbl_word, text=current_word['English'], fill='black')
    flashcard.itemconfig(lbl_language, text="English", fill='black')
    flashcard.itemconfig(flashcard_img, image=flashcard_front)
    flip_timer = root.after(3000, flip_card)


def flip_card():
    flashcard.itemconfig(flashcard_img, image=flashcard_back)
    flashcard.itemconfig(lbl_language, text="Spanish", fill='white')
    flashcard.itemconfig(lbl_word, text=current_word['Spanish'], fill='white')


def known_word():
    words_to_learn.remove(current_word)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv(TO_LEARN, index=False)
    next_word()


root = Tk()
root.title('Flashy')
root.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = root.after(3000, flip_card)
flashcard = Canvas(width=810, height=526,
                   bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard_front = PhotoImage(file=FLASHCARD_IMAGE_FRONT)
flashcard_back = PhotoImage(file=FLASHCARD_IMAGE_BACK)
flashcard_img = flashcard.create_image(400, 265, image=flashcard_front)
lbl_language = flashcard.create_text(
    400, 150, text='English', font=("Courier", 40, ITALIC))
lbl_word = flashcard.create_text(400, 263, font=("Courier", 60, BOLD))
flashcard.grid(row=0, column=0, columnspan=2)

img_right = PhotoImage(file=RIGHT_IMAGE)
btn_right = Button(image=img_right, highlightthickness=0,
                   borderwidth=0, command=known_word)
btn_right.grid(row=1, column=0)

img_wrong = PhotoImage(file=WRONG_IMAGE)
btn_wrong = Button(image=img_wrong, highlightthickness=0,
                   borderwidth=0, command=next_word)
btn_wrong.grid(row=1, column=1)

next_word()

root.mainloop()
