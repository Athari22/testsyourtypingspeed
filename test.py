import tkinter as tk
import random
import time

# List of sentences
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing tests improve speed and accuracy.",
    "Python is a fun language to learn.",
    "Practice makes perfect in everything.",
    "Keep your fingers on the home row keys."
]

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("700x400")
        self.root.config(padx=20, pady=20)

        self.sentence = random.choice(sentences)
        self.start_time = None

        # Widgets
        self.label = tk.Label(root, text="Type the sentence below:", font=("Arial", 16))
        self.label.pack(pady=10)

        self.sentence_label = tk.Label(root, text=self.sentence, wraplength=600, font=("Arial", 14), fg="blue")
        self.sentence_label.pack(pady=10)

        self.entry = tk.Text(root, height=5, width=70, font=("Arial", 12))
        self.entry.pack(pady=10)
        self.entry.bind("<FocusIn>", self.start_timer)

        self.done_button = tk.Button(root, text="Done", command=self.calculate_results, font=("Arial", 12))
        self.done_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
        self.result_label.pack(pady=10)

    def start_timer(self, event):
        if not self.start_time:
            self.start_time = time.time()

    def calculate_results(self):
        end_time = time.time()
        typed_text = self.entry.get("1.0", "end-1c")
        time_taken = end_time - self.start_time if self.start_time else 0

        words = typed_text.split()
        word_count = len(words)
        wpm = (word_count / time_taken) * 60 if time_taken > 0 else 0

        correct_chars = sum(
            1 for i, c in enumerate(typed_text)
            if i < len(self.sentence) and c == self.sentence[i]
        )
        accuracy = (correct_chars / len(self.sentence)) * 100

        result = f"⏱ Time: {time_taken:.2f} sec | 💬 WPM: {wpm:.2f} | 🎯 Accuracy: {accuracy:.2f}%"
        self.result_label.config(text=result)

        # Disable entry and button
        self.entry.config(state="disabled")
        self.done_button.config(state="disabled")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
