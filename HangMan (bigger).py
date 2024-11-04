import tkinter as tk
from tkinter import ttk
import random

def select_word():
    words = ["python", "pandas", "integer", "string", "modulo", "float", "loop", "package", "import", "boolean"]
    return random.choice(words).upper()

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.configure(bg="black")
        root.attributes('-fullscreen', True)
        root.bind("<Escape>", lambda event: root.quit())
        self.word = select_word()
        self.guessed_letters = set()
        self.correct_guesses = set()
        self.attempts = 6
        self.hints_used = 0
        self.score = {"wins": 0, "losses": 0}
        self.game_active = True

        # Display score
        self.score_label = tk.Label(root, text=f"Wins: {self.score['wins']}  Losses: {self.score['losses']}", font=("Helvetica", 16), fg="yellow", bg="black")
        self.score_label.pack(pady=(10, 40))

        # Display word
        self.word_display = tk.StringVar()
        self.label_word = tk.Label(root, textvariable=self.word_display, font=("Courier", 50, "bold"), fg="white", bg="black", anchor="center")
        self.label_word.pack(pady=(20, 40))
        self.update_display()

        # Display attempts
        self.label_attempts = tk.Label(root, text=f"Attempts remaining: {self.attempts}", font=("Helvetica", 20), fg="white", bg="black")
        self.label_attempts.pack(pady=(5, 20))

        # Canvas
        self.canvas = tk.Canvas(root, width=300, height=350, bg='black', highlightthickness=0)
        self.canvas.pack(pady=(5, 20))
        self.draw_hangman(0)

        # Result and correct answer display
        self.result_message = tk.StringVar()
        self.label_result = tk.Label(root, textvariable=self.result_message, font=("Helvetica", 28, "bold"), bg="black", fg="yellow", wraplength=400, anchor="center", justify="center")
        self.label_result.pack_forget()
        self.correct_answer_label = tk.Label(root, text="", font=("Helvetica", 18), bg="black", fg="light gray")
        self.correct_answer_label.pack(pady=(5, 20))

        # Control buttons
        self.button_frame = tk.Frame(root, bg="black")
        style = ttk.Style()
        style.configure("Large.TButton", font=("Helvetica", 18))
        self.button_hint = ttk.Button(self.button_frame, text="Hint", command=self.use_hint, style="Large.TButton")
        self.button_hint.grid(row=0, column=0, padx=10)
        self.button_again = ttk.Button(self.button_frame, text="New Game", command=self.reset_game, style="Large.TButton")
        self.button_again.grid(row=0, column=1, padx=10)
        self.button_end = ttk.Button(self.button_frame, text="Exit", command=root.quit, style="Large.TButton")
        self.button_end.grid(row=0, column=2, padx=10)
        self.button_frame.pack(pady=(10, 20))

        # Alphabetical keypad
        self.keypad_frame = tk.Frame(root, bg="black")
        self.keypad_frame.pack(pady=10)
        self.keypad_buttons = {}
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for row_index in range(3):
            for col_index in range(8):
                letter_index = row_index * 8 + col_index
                if letter_index < len(alphabet):
                    letter = alphabet[letter_index]
                    button = ttk.Button(self.keypad_frame, text=letter, command=lambda l=letter: self.guess_letter(l), style="Large.TButton", width=6)
                    button.grid(row=row_index, column=col_index, padx=5, pady=5)
                    self.keypad_buttons[letter] = button
        root.bind("<Key>", self.keyboard_guess)

    def update_display(self):
        display = [letter if letter in self.guessed_letters else '_' for letter in self.word]
        self.word_display.set(" ".join(display))

    def guess_letter(self, guess):
        if not self.game_active:
            return
        if guess in self.guessed_letters or guess in self.correct_guesses:
            self.display_message(f"You've already guessed '{guess}'", "orange")
            return
        if not guess.isalpha() or len(guess) != 1:
            self.display_message("Invalid input", "orange")
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            self.correct_guesses.add(guess)
            self.update_display()
            self.keypad_buttons[guess].config(state="disabled")
            if all(letter in self.guessed_letters for letter in self.word):
                self.display_message("Congratulations!", "green")
                self.show_correct_answer()
                self.score["wins"] += 1
                self.disable_game()
        else:
            self.attempts -= 1
            self.label_attempts.config(text=f"Attempts remaining: {self.attempts}")
            self.draw_hangman(6 - self.attempts)
            self.keypad_buttons[guess].config(state="disabled")
            if self.attempts == 0:
                self.display_message("Game Over!", "red")
                self.show_correct_answer()
                self.score["losses"] += 1
                self.disable_game()

        self.score_label.config(text=f"Wins: {self.score['wins']}  Losses: {self.score['losses']}")

    def display_message(self, message, color="yellow"):
        self.result_message.set(message)
        self.label_result.config(fg=color)
        self.label_result.pack(pady=(5, 10))

    def hide_message(self):
        self.result_message.set("")
        self.label_result.pack_forget()

    def show_correct_answer(self):
        self.correct_answer_label.config(text=f"The correct word is: {self.word}")

    def use_hint(self):
        if not self.game_active:
            return
        if self.hints_used == 0:
            remaining_letters = [letter for letter in self.word if letter not in self.guessed_letters]
            if remaining_letters:
                hint_letter = random.choice(remaining_letters)
                self.guessed_letters.add(hint_letter)
                self.correct_guesses.add(hint_letter)
                self.hints_used += 1
                self.update_display()
                self.display_message(f"Hint: '{hint_letter}'", "blue")
                self.keypad_buttons[hint_letter].config(state="disabled")
            else:
                self.display_message("No hints available", "orange")
        else:
            self.display_message("Hint already used!", "orange")

    def keyboard_guess(self, event):
        if not self.game_active:
            return
        guess = event.char.upper()
        if guess.isalpha() and len(guess) == 1:
            self.guess_letter(guess)
        else:
            self.display_message("Invalid input", "orange")

    def disable_game(self):
        self.button_hint.config(state="disabled")
        self.game_active = False

    def reset_game(self):
        self.word = select_word()
        self.guessed_letters.clear()
        self.correct_guesses.clear()
        self.attempts = 6
        self.hints_used = 0
        self.hide_message()
        self.correct_answer_label.config(text="")
        self.label_result.config(text="", fg="yellow")
        self.update_display()
        self.label_attempts.config(text=f"Attempts remaining: {self.attempts}")
        self.canvas.delete("all")
        self.draw_hangman(0)
        self.button_hint.config(state="normal")
        self.game_active = True

        for button in self.keypad_buttons.values():
            button.config(state="normal")

    def draw_hangman(self, stage):
        self.canvas.delete("all")
        if stage >= 0:
            self.canvas.create_line(50, 300, 250, 300, fill="white", width=4)
        if stage >= 1:
            self.canvas.create_line(100, 300, 100, 50, fill="white", width=4)
        if stage >= 2:
            self.canvas.create_line(100, 50, 200, 50, fill="white", width=4)
        if stage >= 3:
            self.canvas.create_line(200, 50, 200, 80, fill="white", width=4)
        if stage >= 4:
            self.canvas.create_oval(180, 80, 220, 120, outline="white", width=4)
        if stage >= 5:
            self.canvas.create_line(200, 120, 200, 200, fill="white", width=4)
        if stage >= 6:
            self.canvas.create_line(200, 140, 170, 160, fill="white", width=4)
        if stage >= 7:
            self.canvas.create_line(200, 140, 230, 160, fill="white", width=4)
        if stage >= 8:
            self.canvas.create_line(200, 200, 180, 250, fill="white", width=4)
        if stage >= 9:
            self.canvas.create_line(200, 200, 220, 250, fill="white", width=4)

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
