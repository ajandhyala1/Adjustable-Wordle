import tkinter as tk
from tkinter import messagebox
import random

# Define the word list
WORD_LIST = ["apple", "banjo", "candy", "dogma", "eagle", "flame", "grape", "honey", "ivory", "joker"]

def load_word_list(word_length):
    # Filter words that match the desired length
    return [word for word in WORD_LIST if len(word) == word_length]

def choose_word(word_list):
    # Randomly select a word from the word list
    return random.choice(word_list)

def get_feedback(secret_word, guess):
    feedback = []
    for i, char in enumerate(guess):
        if char == secret_word[i]:
            feedback.append('G')  # Green for correct letter in correct place
        elif char in secret_word:
            feedback.append('Y')  # Yellow for correct letter in wrong place
        else:
            feedback.append('B')  # Black for incorrect letter
    return ''.join(feedback)

def start_game():
    try:
        word_length = int(word_length_entry.get())
        max_guesses = int(max_guesses_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers.")
        return
    
    word_list = load_word_list(word_length)
    if not word_list:
        messagebox.showerror("No words found", f"No words of length {word_length} available.")
        return
    
    global secret_word, guesses_left, max_guesses_allowed, guess_entries, feedback_labels
    secret_word = choose_word(word_list)
    guesses_left = max_guesses
    max_guesses_allowed = max_guesses
    
    for widget in game_frame.winfo_children():
        widget.destroy()
    
    tk.Label(game_frame, text=f"Guess the {word_length}-letter word").pack()

    guess_entries = []
    feedback_labels = []
    
    for i in range(max_guesses):
        guess_frame = tk.Frame(game_frame)
        guess_frame.pack(pady=2)
        
        guess_entry = tk.Entry(guess_frame, width=word_length, font=('Arial', 14))
        guess_entry.pack(side='left')
        guess_entries.append(guess_entry)
        
        feedback_label = tk.Label(guess_frame, text="", font=('Arial', 14))
        feedback_label.pack(side='left', padx=10)
        feedback_labels.append(feedback_label)
    
    guess_button = tk.Button(game_frame, text="Guess", command=make_guess)
    guess_button.pack(pady=10)

def make_guess():
    global guesses_left
    guess = guess_entries[max_guesses_allowed - guesses_left].get().strip().lower()
    
    if len(guess) != len(secret_word):
        messagebox.showerror("Invalid guess", f"Your guess must be {len(secret_word)} letters long.")
        return
    
    feedback = get_feedback(secret_word, guess)
    feedback_labels[max_guesses_allowed - guesses_left].config(text=feedback)
    
    if guess == secret_word:
        messagebox.showinfo("Congratulations!", "You guessed the word correctly!")
        reset_game()
        return
    
    guesses_left -= 1
    
    if guesses_left == 0:
        messagebox.showinfo("Game Over", f"Sorry, you've used all your guesses. The word was '{secret_word}'.")
        reset_game()

def reset_game():
    for entry in guess_entries:
        entry.config(state='disabled')
    for label in feedback_labels:
        label.config(state='disabled')

# Set up the main window
root = tk.Tk()
root.title("Wordle Game")

# Input frame for word length and number of guesses
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Word Length:").grid(row=0, column=0, padx=5)
word_length_entry = tk.Entry(input_frame, width=5)
word_length_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Number of Guesses:").grid(row=1, column=0, padx=5)
max_guesses_entry = tk.Entry(input_frame, width=5)
max_guesses_entry.grid(row=1, column=1, padx=5)

start_button = tk.Button(input_frame, text="Start Game", command=start_game)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

# Frame for the game interface
game_frame = tk.Frame(root)
game_frame.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
