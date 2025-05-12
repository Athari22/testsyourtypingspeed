import tkinter as tk
from tkinter import messagebox
import random
import time

# Constants
FONT_NAME = "Courier"
BG_COLOR = '#F1EFEC'
BUTTON_COLOR = '#D4C9BE'
TEXT_COLOR = '#123458'


# Load random text from file
def load_random_text():
    try:
        with open("file.txt", "r") as file:
            paragraphs = file.read().split("\n\n")
            return random.choice(paragraphs).strip()
    except FileNotFoundError:
        messagebox.showerror("Error", "file.txt not found!")
        return ""


# Timer and test logic
def start_test():
    global timer_running, typed_started, start_time, remaining_time
    if not typed_started:
        typed_started = True
        start_button.config(state="disabled")  # Disable the start button after clicking
        text_area.config(state="normal")  # Enable text_area for typing
        text_area.delete("1.0", "end-1c")  # Clear text area
        text_area.focus()  # Set focus to the text area for typing
        start_time = time.time()  # Record the start time
        remaining_time = 60  # Set initial time to 60 seconds
        update_timer()  # Start the timer
        window.after(1000, update_score)  # Update score every second


def update_timer():
    global remaining_time
    if remaining_time > 0:
        remaining_time -= 1
        timer_label.config(text=f"Time Left: {remaining_time} seconds")
        window.after(1000, update_timer)  # Call the update_timer every second
    else:
        end_test()  # End test when time is up


def update_score():
    typed_text = text_area.get("1.0", "end-1c").strip().split()
    reference_text = text_display.get("1.0", "end-1c").strip().split()
    
    # Calculate correct words typed
    correct_words = sum(1 for i, word in enumerate(typed_text) if i < len(reference_text) and word == reference_text[i])
    
    # Calculate typing speed (WPM)
    elapsed_time = time.time() - start_time
    wpm = (correct_words / elapsed_time) * 60  # Calculate words per minute
    
    # Display the WPM score
    score_label.config(text=f"Your Speed: {wpm:.2f} WPM\nCorrect Words: {correct_words}")
    
    if remaining_time > 0:
        window.after(1000, update_score)  # Update score every second


def end_test():
    global typed_started
    typed_started = False
    typed_text = text_area.get("1.0", "end-1c").strip().split()
    reference_text = text_display.get("1.0", "end-1c").strip().split()
    
    # Calculate correct words typed
    correct_words = sum(1 for i, word in enumerate(typed_text) if i < len(reference_text) and word == reference_text[i])
    
    # Calculate typing speed (WPM)
    elapsed_time = time.time() - start_time
    wpm = (correct_words / elapsed_time) * 60  # Calculate words per minute
    
    # Display results
    result_label.config(text=f"Test Over!\nYour Speed: {wpm:.2f} WPM\nCorrect Words: {correct_words}")
    text_area.config(state="disabled")  # Disable text_area after the test


def restart_test():
    global typed_started
    typed_started = False
    text_area.delete("1.0", tk.END)
    new_text = load_random_text()
    text_display.config(state="normal")
    text_display.delete("1.0", tk.END)
    text_display.insert("1.0", new_text)
    text_display.config(state="disabled")
    result_label.config(text="")
    start_button.config(state="normal")  # Re-enable the start button
    timer_label.config(text="Time Left: 60 seconds")
    score_label.config(text="Your Speed: 0 WPM\nCorrect Words: 0")


# Main window setup
window = tk.Tk()
window.title("Typing Speed Test")
window.config(padx=100, pady=50, bg=BG_COLOR)

typed_started = False
timer_running = False
remaining_time = 60  # Time for the typing test

# Title
title_label = tk.Label(window, text="Test your typing speed", font=(FONT_NAME, 24, "bold"), fg="#5A6C57", bg=BG_COLOR)
title_label.grid(column=0, row=0, columnspan=3, pady=10)

# Reference Text Display
text_display = tk.Text(window, height=7, width=70, wrap=tk.WORD, font=(FONT_NAME, 12), state="disabled", bg="#ffffff")
text_display.grid(column=0, row=1, columnspan=3, pady=10)

# Typing Text Area
text_area = tk.Text(window, height=7, width=70, wrap=tk.WORD, font=(FONT_NAME, 12), state="disabled")
text_area.grid(column=0, row=2, columnspan=3, pady=10)

# Timer Label
timer_label = tk.Label(window, text="Time Left: 60 seconds", font=(FONT_NAME, 14), fg=TEXT_COLOR, bg=BG_COLOR)
timer_label.grid(column=0, row=3, columnspan=3)

# Score Label
score_label = tk.Label(window, text="Your Speed: 0 WPM\nCorrect Words: 0", font=(FONT_NAME, 14), fg=TEXT_COLOR,
                       bg=BG_COLOR)
score_label.grid(column=0, row=4, columnspan=3)

# Result Label
result_label = tk.Label(window, text="", font=(FONT_NAME, 14), fg=TEXT_COLOR, bg=BG_COLOR)
result_label.grid(column=0, row=5, columnspan=3)

# Buttons
button_style = {
    'highlightthickness': 0,
    'width': 15,
    'height': 2,
    'font': ("Arial", 12),
    'bg': BUTTON_COLOR,
    'fg': TEXT_COLOR,
    'activebackground': "#45a049",
    'activeforeground': "#030303",
    'relief': "raised"
}

# Start Button
start_button = tk.Button(window, text="Start", command=start_test, **button_style)
start_button.grid(column=0, row=6, padx=10, pady=10)

# Restart Button
restart_button = tk.Button(window, text="Restart", command=restart_test, **button_style)
restart_button.grid(column=1, row=6, padx=10, pady=10)

# Load initial text
restart_test()

window.mainloop()


