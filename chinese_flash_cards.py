from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
word_choice = {}
data_dict = {}
hsk_level = ""


# -------------------------- choose level -------------------------- #
def choose():
    hsk_level_window.destroy()
    global hsk_level
    hsk_level = level.get()


hsk_level_window = Tk()
level = StringVar(hsk_level_window, "hsk1")
hsk_level_window.title("HSK Level")
hsk_level_window.config(background=BACKGROUND_COLOR, padx=40, pady=40)
hsk_level_canvas = Canvas(hsk_level_window, background=BACKGROUND_COLOR, highlightthickness=0, width=200, height=40)
font_preset = ("Arial", 15, "normal")
hsk_level_canvas.create_text(100, 20, text="Choose HSK level:", font=font_preset)
hsk_level_canvas.grid(row=0)
one = Radiobutton(hsk_level_window, background=BACKGROUND_COLOR, text="HSK 1", variable=level, value="hsk1", font=font_preset)
two = Radiobutton(hsk_level_window, background=BACKGROUND_COLOR, text="HSK 2", variable=level, value="hsk2", font=font_preset)
three = Radiobutton(hsk_level_window, background=BACKGROUND_COLOR, text="HSK 3", variable=level, value="hsk3", font=font_preset)
four = Radiobutton(hsk_level_window, background=BACKGROUND_COLOR, text="HSK 4", variable=level, value="hsk4", font=font_preset)
five = Radiobutton(hsk_level_window, background=BACKGROUND_COLOR, text="HSK 5", variable=level, value="hsk5", font=font_preset)
six = Radiobutton(hsk_level_window, background=BACKGROUND_COLOR, text="HSK 6", variable=level, value="hsk6", font=font_preset)
one.grid(row=1)
two.grid(row=2)
three.grid(row=3)
four.grid(row=4)
five.grid(row=5)
six.grid(row=6)
hsk_choose = Button(hsk_level_window, text="Choose this level", highlightthickness=0, command=choose, font=font_preset)
hsk_choose.grid(row=7)
hsk_level_window.mainloop()


# ---------------------------- read CSV -----------------------------------#
def read_csv():
    global data_dict
    try:
        data = pd.read_csv(f"data/chinese/words_to_learn_{hsk_level}.csv")
    except FileNotFoundError:
        original_data = pd.read_csv(f"data/chinese/chinese_words_{hsk_level}.csv")
        data_dict = original_data.to_dict(orient="records")
    else:
        data_dict = data.to_dict(orient="records")


# ---------------------------- functions -----------------------------------#
next_card_is_showing = True


def next_card():
    global word_choice, flip_timer, next_card_is_showing
    next_card_is_showing = True
    window.after_cancel(flip_timer)
    try:
        word_choice = random.choice(data_dict)
        canvas.itemconfig(canvas_image, image=flash_card_front)
        # show/hide pinyin according to radiobutton
        show_function()
        flip_timer = window.after(5000, func=flip_card)
    except IndexError:
        canvas.itemconfig(title_text, text="Congratulations!", fill="black")
        canvas.itemconfig(word_text, text=f"You've mastered {hsk_level.upper()}!\nPress any button to restart.",
                          fill="black")
        read_csv()


def is_known():
    try:
        data_dict.remove(word_choice)
        # print(len(data_dict))
        data = pd.DataFrame(data_dict)
        data.to_csv(f"data/chinese/words_to_learn_{hsk_level}.csv", index=False)
        next_card()
    except ValueError:
        reset()
    canvas.itemconfig(words_left, text=f"Words to learn: {len(data_dict)}", fill="black")
    


def show_function():
    if next_card_is_showing:
        canvas.itemconfig(title_text, text=f"{word_choice['hanzi']}", fill="black")
        if show.get():
            canvas.itemconfig(word_text, text=f"{word_choice['pinyin']}", fill="black")
        else:
            canvas.itemconfig(word_text, text="", fill="black")


def flip_card():
    global next_card_is_showing
    if next_card_is_showing:
        canvas.itemconfig(canvas_image, image=flash_card_back)
        canvas.itemconfig(title_text, text=f"{word_choice['hanzi']}", fill="white")
        canvas.itemconfig(word_text, text=f"{word_choice['meaning']}", fill="white")
        next_card_is_showing = False
    else:
        canvas.itemconfig(canvas_image, image=flash_card_front)
        canvas.itemconfig(title_text, text=f"{word_choice['hanzi']}", fill="black")
        canvas.itemconfig(word_text, text=f"{word_choice['pinyin']}", fill="black")
        next_card_is_showing = True

def reset():
    global data_dict
    og_data = pd.read_csv(f"data/chinese/chinese_words_{hsk_level}.csv")
    data_dict = og_data.to_dict(orient="records")
    pd.DataFrame(data_dict).to_csv(f"data/chinese/words_to_learn_{hsk_level}.csv", index=False)
    canvas.itemconfig(words_left, text=f"Words to learn: {len(data_dict)}", fill="black")
    next_card()

# ---------------------------- UI -----------------------------------#

read_csv()

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

flip_timer = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=526)
flash_card_front = PhotoImage(file="images/card_front.png")
flash_card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=flash_card_front)

title_text = canvas.create_text(400, 150, text="", font=("Arial", 60, "bold"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 40, "normal"), width=760)
level_text = canvas.create_text(60, 30, text=f"{hsk_level.upper()}", font=("Arial", 20, "normal"))
words_left = canvas.create_text(620, 30, text=f"Words to learn: {len(data_dict)}", font=("Arial", 20, "normal"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=3)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=2, row=1)

# Choose whether to show/hide pinyin
show = BooleanVar(window, True)
show_pinyin_canvas = Canvas()
show_pinyin_canvas.config(bg=BACKGROUND_COLOR, background=BACKGROUND_COLOR, highlightthickness=0)
show_pinyin = Radiobutton(show_pinyin_canvas, background=BACKGROUND_COLOR, text="Show pīnyīn", fg="black",
                          variable=show, value=True, font="Arial", activebackground=BACKGROUND_COLOR)
hide_pinyin = Radiobutton(show_pinyin_canvas, background=BACKGROUND_COLOR, text="Hide pīnyīn", fg="black",
                          variable=show, value=False, font="Arial", activebackground=BACKGROUND_COLOR)
show_button = Button(show_pinyin_canvas, text="Apply", highlightthickness=0, font="Arial", command=show_function)
flip_button = Button(show_pinyin_canvas, text="Flip Card", highlightthickness=0, font="Arial", command=flip_card)
reset_button = Button(show_pinyin_canvas, text="Reset", highlightthickness=0, font="Arial", command=reset)
show_pinyin_canvas.grid(column=1, row=1)
show_pinyin.grid(column=0, row=0)
hide_pinyin.grid(column=0, row=1)
show_button.grid(column=0, row=2)
flip_button.grid(column=0, row=3)
reset_button.grid(column=0, row=4)
next_card()

window.mainloop()
