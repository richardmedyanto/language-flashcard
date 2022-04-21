from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
word_choice = {}
data_dict = {}

#---------------------------- read CSV -----------------------------------#
try:
    data = pd.read_csv("data/french/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")


#---------------------------- functions -----------------------------------#
def next_card():
    global word_choice, flip_timer
    window.after_cancel(flip_timer)
    word_choice = random.choice(data_dict)
    canvas.itemconfig(canvas_image, image=flash_card_front)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=f"{word_choice['French']}", fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=flash_card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=f"{word_choice['English']}", fill="white")


def is_known():
    data_dict.remove(word_choice)
    # print(len(data_dict))
    data = pd.DataFrame(data_dict)
    data.to_csv("data/french/words_to_learn.csv", index=False)
    next_card()

#---------------------------- UI -----------------------------------#


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
flash_card_front = PhotoImage(file="images/card_front.png")
flash_card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=flash_card_front)

title_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()