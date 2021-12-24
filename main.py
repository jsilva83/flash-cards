# Import external modules.
import tkinter
import pandas as pd
import random

# Global variables.
global french_words_df
global card_canvas
global a_text_canvas
global b_text_canvas

# Constants.
BACKGROUND_COLOR = "#B1DDC6"


def flash_card():
    """Returns a random card and updates the canvas."""
    global french_words_df
    global card_canvas
    global a_text_canvas
    global b_text_canvas
    card_deck_size = french_words_df['French'].size
    card_nr = random.randint(0, card_deck_size - 1)
    french_word = french_words_df.at[card_nr, 'French']
    card_canvas.itemconfig(b_text_canvas, text='French')
    card_canvas.itemconfig(b_text_canvas, text=french_word)
    return


def app_gui():
    """Creates the gui and controls its execution."""
    global french_words_df
    global card_canvas
    global a_text_canvas
    global b_text_canvas
    # Create window.
    root_window = tkinter.Tk()
    root_window.config(
        bg=BACKGROUND_COLOR,
        padx=50,
        pady=50,
    )
    root_window.title('Flashy')
    # Create variables with images for buttons.
    card_front_image = tkinter.PhotoImage(file='./images/card_front.png')
    card_back_image = tkinter.PhotoImage(file='./images/card_back.png')
    x_image = tkinter.PhotoImage(file='./images/wrong.png')
    v_image = tkinter.PhotoImage(file='./images/right.png')
    # Create the canvas.
    card_canvas = tkinter.Canvas(root_window)
    card_canvas.config(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
    card_canvas.create_image(0, 0, image=card_front_image, anchor='nw')
    a_text_canvas = card_canvas.create_text(400, 150, text='Title', fill='black', font=('Ariel', 40, 'italic'))
    b_text_canvas = card_canvas.create_text(400, 263, text='word', fill='black', font=('Ariel', 60, 'bold'))
    card_canvas.grid(row=0, column=0, columnspan=2)
    # Create wrong button.
    wrong_button = tkinter.Button(root_window)
    wrong_button.config(image=x_image, highlightthickness=0, command=flash_card)
    wrong_button.grid(row=1, column=0)
    # Create right button.
    right_button = tkinter.Button(root_window)
    right_button.config(image=v_image, highlightthickness=0, command=flash_card)
    right_button.grid(row=1, column=1)
    # Read the cards from file.
    french_words_df = pd.read_csv('./data/french_words.csv')
    # Start the game by flashing the cards.
    flash_card()
    # Wait for events.
    root_window.mainloop()
    return


def main():
    """Runs the main code and orchestration."""
    app_gui()
    return


if __name__ == '__main__':
    """If executed as main component application run main()."""
    main()
