from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
def chinese():
    main_menu.destroy()
    import chinese_flash_cards

def japanese():
    main_menu.destroy()
    import japanese_flash_cards

def french():
    main_menu.destroy()
    import french_flash_cards

main_menu = Tk()
main_menu.title("Flashy")
width_loc = 250
main_menu.config(padx=40, pady=40, background=BACKGROUND_COLOR)
canvas = Canvas(main_menu, width=width_loc, height=50, background=BACKGROUND_COLOR, highlightthickness=0)
text = canvas.create_text(width_loc/2, 10, text="Choose language to learn: ", font="Arial")
chinese_button = Button(main_menu, text="Chinese", command=chinese, font="Arial")
japanese_button = Button(main_menu, text="Japanese", command=japanese, font="Arial")
french_button = Button(main_menu, text="French", command=french, font="Arial")
canvas.grid(row=0)
chinese_button.grid(row=1)
japanese_button.grid(row=2)
french_button.grid(row=3)
main_menu.mainloop()