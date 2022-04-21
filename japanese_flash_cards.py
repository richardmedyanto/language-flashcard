from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
word_choice = {}
data_dict = {}
jlpt_level = ""


def choose():
    jlpt_level_window.destroy()
    global jlpt_level
    jlpt_level = level.get()


jlpt_level_window = Tk()
level = StringVar(jlpt_level_window, "n5")
jlpt_level_window.title("JLPT Level")
jlpt_level_window.config(background=BACKGROUND_COLOR, padx=40, pady=40)
jlpt_level_canvas = Canvas(jlpt_level_window, background=BACKGROUND_COLOR, highlightthickness=0, width=200, height=40)
font_preset = ("Arial", 15, "normal")
jlpt_level_canvas.create_text(100, 20, text="Choose level:", font=font_preset)
jlpt_level_canvas.grid(row=0)
five = Radiobutton(jlpt_level_window, background=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, text="N5",
                   variable=level, value="n5", font=font_preset)
four = Radiobutton(jlpt_level_window, background=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, text="N4",
                   variable=level, value="n4", font=font_preset)
three = Radiobutton(jlpt_level_window, background=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, text="N3",
                    variable=level, value="n3", font=font_preset)
two = Radiobutton(jlpt_level_window, background=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, text="N2",
                  variable=level, value="n2", font=font_preset)
one = Radiobutton(jlpt_level_window, background=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR, text="N1",
                  variable=level, value="n1", font=font_preset)
five.grid(row=1)
four.grid(row=2)
three.grid(row=3)
two.grid(row=4)
one.grid(row=5)
hsk_choose = Button(jlpt_level_window, text="Choose this level", highlightthickness=0, command=choose, font=font_preset)
hsk_choose.grid(row=7)
jlpt_level_window.mainloop()


# ---------------------------- read CSV -----------------------------------#
def read_csv():
    global data_dict
    try:
        data = pd.read_csv(f"data/japanese/words_to_learn_{jlpt_level}.csv")
    except FileNotFoundError:
        original_data = pd.read_csv(f"data/japanese/japanese_words_{jlpt_level}.csv")
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
        show_function()
        flip_timer = window.after(5000, func=flip_card)
    except IndexError:
        canvas.itemconfig(title_text, text="Congratulations!", fill="black")
        canvas.itemconfig(word_text, text=f"You've mastered {jlpt_level.upper()}!\nPress any button to restart.",
                          fill="black")
        read_csv()


def is_known():
    try:
        data_dict.remove(word_choice)
        # print(len(data_dict))
        data = pd.DataFrame(data_dict)
        data.to_csv(f"data/japanese/words_to_learn_{jlpt_level}.csv", index=False)
        next_card()
    except ValueError:
        og_data = pd.read_csv(f"data/japanese/japanese_words_{jlpt_level}.csv")
        data_d = og_data.to_dict(orient="records")
        pd.DataFrame(data_d).to_csv(f"data/japanese/words_to_learn_{jlpt_level}.csv", index=False)
        next_card()
    canvas.itemconfig(words_left, text=f"Words to learn: {len(data_dict)}", fill="black")


def show_function():
    if next_card_is_showing:
        canvas.itemconfig(title_text, text=f"{word_choice['kanji']}", fill="black")
        if show.get():
            canvas.itemconfig(word_text, text=f"{word_choice['kana']}", fill="black")
        else:
            canvas.itemconfig(word_text, text="", fill="black")

def flip_card():
    global next_card_is_showing
    if next_card_is_showing:
        canvas.itemconfig(canvas_image, image=flash_card_back)
        canvas.itemconfig(title_text, text=f"{word_choice['kanji']}", fill="white")
        canvas.itemconfig(word_text, text=f"{word_choice['meaning']}", fill="white")
        next_card_is_showing = False
    else:
        canvas.itemconfig(canvas_image, image=flash_card_front)
        canvas.itemconfig(title_text, text=f"{word_choice['kanji']}", fill="black")
        canvas.itemconfig(word_text, text=f"{word_choice['kana']}", fill="black")
        next_card_is_showing = True

def reset():
    global data_dict
    og_data = pd.read_csv(f"data/japanese/japanese_words_{jlpt_level}.csv")
    data_dict = og_data.to_dict(orient="records")
    pd.DataFrame(data_dict).to_csv(f"data/japanese/words_to_learn_{jlpt_level}.csv", index=False)
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
level_text = canvas.create_text(50, 30, text=f"{jlpt_level.upper()}", font=("Arial", 20, "normal"))
words_left = canvas.create_text(620, 30, text=f"Words to learn: {len(data_dict)}", font=("Arial", 20, "normal"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=3)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=2, row=1)

# Choose whether to show/hide kana
show = BooleanVar(window, True)
show_kana_canvas = Canvas()
show_kana_canvas.config(bg=BACKGROUND_COLOR, background=BACKGROUND_COLOR, highlightthickness=0)
show_kana = Radiobutton(show_kana_canvas, background=BACKGROUND_COLOR, text="Show kana", fg="black",
                        variable=show, value=True, font="Arial", activebackground=BACKGROUND_COLOR)
hide_kana = Radiobutton(show_kana_canvas, background=BACKGROUND_COLOR, text="Hide kana", fg="black",
                        variable=show, value=False, font="Arial", activebackground=BACKGROUND_COLOR)
show_button = Button(show_kana_canvas, text="Apply", highlightthickness=0, font="Arial", command=show_function)
flip_button = Button(show_kana_canvas, text="Flip Card", highlightthickness=0, font="Arial", command=flip_card)
reset_button = Button(show_kana_canvas, text="Reset", highlightthickness=0, font="Arial", command=reset)
show_kana_canvas.grid(column=1, row=1)
show_kana.grid(column=0, row=0)
hide_kana.grid(column=0, row=1)
show_button.grid(column=0, row=2)
flip_button.grid(column=0, row=3)
reset_button.grid(column=0, row=4)

next_card()

window.mainloop()
