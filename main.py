from tkinter import *
import pandas
import random
import os

translation = {}
data_dict = {}
try:
    words_to_learn = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words_to_learn = pandas.read_csv("data/data.csv")
    data_dict = words_to_learn.to_dict(orient="records")
else:
    data_dict = words_to_learn.to_dict(orient="records")


def delete_progress():
    global data_dict
    try:
        os.remove("data/words_to_learn.csv")
    except FileNotFoundError:
        pass
    else:
        change_word()
        words_to_learn = pandas.read_csv("data/data.csv")
        data_dict = words_to_learn.to_dict(orient="records")


def flip_card():
    canvas.itemconfig(image, image=back_card)
    canvas.itemconfig(language, text="English")
    canvas.itemconfig(word, text=translation["English"])


def change_word():
    global translation, flip_timer
    window.after_cancel(flip_timer)
    translation = random.choice(data_dict)
    canvas.itemconfig(image, image=front_card)
    canvas.itemconfig(language, text="French")
    canvas.itemconfig(word, text=translation["French"])
    flip_timer = window.after(3000, func=flip_card)


def remove_word():
    data_dict.remove(translation)
    print(len(data_dict))
    words_to_learn = pandas.DataFrame(data_dict)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    change_word()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg="white")
flip_timer = window.after(3000, func=flip_card)

front_card = PhotoImage(file="images/frontCard.png")
back_card = PhotoImage(file="images/backCard.png")
canvas = Canvas(width=600, height=426, highlightthickness=0)
image = canvas.create_image(300, 213, image=front_card)

font = ("Ariel", 32, "italic")
language = canvas.create_text(300, 175, text="", font=font)

font = ("Ariel", 45, "bold")
word = canvas.create_text(300, 250, text="", font=font)

canvas.grid(row=0, column=0, columnspan=2)

image_x = PhotoImage(file="images/x-button.png")
button_x = Button(image=image_x, bd=0, width=100, height=80, bg="white", highlightthickness=0, command=change_word)
button_x.grid(row=1, column=0)

image_check = PhotoImage(file="images/checked.png")
button_check = Button(image=image_check, bd=0, width=100, height=80, bg="white", highlightthickness=0,
                      command=remove_word)
button_check.grid(row=1, column=1)

image_refresh = PhotoImage(file="images/refreshing.png")
button_refresh = Button(image=image_refresh, bd=0, width=100, height=80, bg="white", highlightthickness=0,
                        command=delete_progress)
button_refresh.grid(row=2, column=0, columnspan=2)
change_word()

window.mainloop()
