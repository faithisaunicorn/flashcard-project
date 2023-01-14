from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"

# ---------------------------- DATA ------------------------------- #
current_card = {}
revision = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    revision = original_data.to_dict(orient="records")
else:
    revision = data.to_dict(orient = 'records')

# ---------------------------- BUTTONS ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(revision)
    canvas.itemconfig(card_title, text = "French", fill = "black")
    canvas.itemconfig(card_word, text = current_card['French'], fill = "black")
    canvas.itemconfig(card_background, image = front_card)
    flip_timer = window.after(3000, func = flip_card)

def flip_card():
    canvas.itemconfig(card_title, text = "English", fill = "white")
    canvas.itemconfig(card_word, text = current_card['English'], fill = "white")
    canvas.itemconfig(card_background, image = back_card)

def correct(): #if correct, remove from revision deck
    revision.remove(current_card)
    data = pandas.DataFrame(revision)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy McFlashcardFace")
window.config(padx = 50, pady = 50, bg = BACKGROUND_COLOR)

flip_timer = window.after(3000, func = flip_card)

###Canvas is the flash card pic
canvas = Canvas(width=800, height=526, bg = BACKGROUND_COLOR, highlightthickness = 0)
front_card = PhotoImage(file= "images/card_front.png")
back_card = PhotoImage(file = "images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_card)
canvas.grid(column=1, row=1, columnspan=2)

#Words on canvas
card_title = canvas.create_text(400, 150, font=(FONT_NAME,40,"italic"))
card_word = canvas.create_text(400, 263, font=(FONT_NAME,60,"bold"))

#Buttons
right_image = PhotoImage(file = "images/right.png")
right_button = Button(image = right_image, command=correct, highlightthickness = 0)
right_button.grid(column = 2, row = 2)

wrong_image = PhotoImage(file = "images/wrong.png")
wrong_button = Button(image = wrong_image, command=next_card, highlightthickness = 0)
wrong_button.grid(column = 1, row = 2)


next_card()

window.mainloop()