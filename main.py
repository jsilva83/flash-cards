# Import external modules.
import tkinter
import pandas as pd
import random

# Global variables.
global dictionary_words_df
global card_canvas
global title_text_canvas
global center_text_canvas
global down_text_canvas
global card_nr
global root_window
global x_image
global v_image
global canvas_image_item
global card_back_image
global card_front_image
global scheduled_job_id

# Constants.
BACKGROUND_COLOR = '#B1DDC6'
ORIGINAL_WORD_COLOR = '#f62763'
DICT_ORIGINAL_LANGUAGE = 'English'
DICT_TARGET_LANGUAGE = 'Portuguese'
FILE_DICT_REMAINING_WORDS = './data/words_to_learn.csv'
FILE_DICT_INITIAL_WORDS = './data/2800_english_words.csv'


def flip_card():
    """Flips the card with English word translation."""
    global canvas_image_item
    global card_back_image
    global card_front_image
    global title_text_canvas
    global center_text_canvas
    global down_text_canvas
    card_canvas.itemconfig(canvas_image_item, image=card_back_image)
    card_canvas.itemconfig(title_text_canvas, text=DICT_TARGET_LANGUAGE, fill='white')
    card_canvas.itemconfig(center_text_canvas, text=dictionary_words_df.at[card_nr, DICT_TARGET_LANGUAGE], fill='white')
    card_canvas.itemconfig(down_text_canvas,
                           text=dictionary_words_df.at[card_nr, DICT_ORIGINAL_LANGUAGE],
                           fill=ORIGINAL_WORD_COLOR,
                           )
    return


def flash_card(button_pressed):
    """Returns a random card and updates the canvas."""
    global dictionary_words_df
    global card_canvas
    global title_text_canvas
    global center_text_canvas
    global card_nr
    global root_window
    global scheduled_job_id
    try:
        root_window.after_cancel(scheduled_job_id)
    except NameError:
        pass
    # If the user pressed the right button then remove the word / row from dataframe.
    # If it is initiating, then do not execute.
    if button_pressed != 'ini' and button_pressed == 'right':
        dictionary_words_df.drop(
            labels=[card_nr],  # list of indexes to delete.
            axis=0,  # 0 means rows, 1 means columns.
            inplace=True,  # update the dataframe.
        )
        # Reindexing the remaining rows to start from 0 to size of df.
        dictionary_words_df.reset_index(
            drop=True,
            inplace=True,
        )
    # Select next card and update the gui.
    card_deck_size = dictionary_words_df[DICT_ORIGINAL_LANGUAGE].size
    card_nr = random.randint(0, card_deck_size - 1)
    original_word = dictionary_words_df.at[card_nr, DICT_ORIGINAL_LANGUAGE]
    card_canvas.itemconfig(canvas_image_item, image=card_front_image)
    card_canvas.itemconfig(title_text_canvas, text=DICT_ORIGINAL_LANGUAGE, fill='black')
    card_canvas.itemconfig(center_text_canvas, text=original_word, fill='black')
    card_canvas.itemconfig(down_text_canvas, text='', fill=ORIGINAL_WORD_COLOR)
    # Launch a new job to flip the card after 3000 millisenconds.
    scheduled_job_id = root_window.after(5000, flip_card)
    return


def on_closing():
    """What to do when closing the application.\nWhen closing the applications write the unkown words to a file."""
    global dictionary_words_df
    global root_window
    # Write unknown words to a file.
    dictionary_words_df.to_csv(FILE_DICT_REMAINING_WORDS, index=False)
    root_window.destroy()
    return


def app_gui():
    """Creates the gui and controls its execution."""
    global dictionary_words_df
    global card_canvas
    global title_text_canvas
    global center_text_canvas
    global down_text_canvas
    global root_window
    global x_image
    global v_image
    global canvas_image_item
    global card_back_image
    global card_front_image
    # Create window.
    root_window = tkinter.Tk()
    root_window.config(
        bg=BACKGROUND_COLOR,
        padx=50,
        pady=50,
    )
    root_window.title('Flashy')
    root_window.protocol("WM_DELETE_WINDOW", on_closing)
    # Create variables with images for buttons.
    card_front_image = tkinter.PhotoImage(file='./images/card_front.png')
    card_back_image = tkinter.PhotoImage(file='./images/card_back.png')
    x_image = tkinter.PhotoImage(file='./images/wrong.png')
    v_image = tkinter.PhotoImage(file='./images/right.png')
    # Create the canvas.
    card_canvas = tkinter.Canvas(root_window)
    card_canvas.config(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas_image_item = card_canvas.create_image(0, 0, image=card_front_image, anchor='nw')
    title_text_canvas = card_canvas.create_text(400, 150, text='Title', fill='black', font=('Ariel', 40, 'italic'))
    center_text_canvas = card_canvas.create_text(400, 263, text='word', fill='black', font=('Ariel', 60, 'bold'))
    down_text_canvas = card_canvas.create_text(400, 363, text='', fill='black', font=('Ariel', 50, 'italic'))
    card_canvas.grid(row=0, column=0, columnspan=2)
    # Create wrong button.
    wrong_button = tkinter.Button(root_window)
    wrong_button.config(
        image=x_image,
        bg=BACKGROUND_COLOR,
        highlightthickness=0,
        borderwidth=0,
        command=lambda: flash_card('wrong'),
    )
    wrong_button.grid(row=1, column=0)
    # Create right button.
    right_button = tkinter.Button(root_window)
    right_button.config(
        image=v_image,
        bg=BACKGROUND_COLOR,
        highlightthickness=0,
        borderwidth=0,
        command=lambda: flash_card('right'),
    )
    right_button.grid(row=1, column=1)
    # Read the cards from file from words_to_learn if it exists.
    try:
        dictionary_words_df = pd.read_csv(FILE_DICT_REMAINING_WORDS)
    except FileNotFoundError:
        dictionary_words_df = pd.read_csv(FILE_DICT_INITIAL_WORDS)
    # Start the game by flashing the cards.
    flash_card('init')
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
