import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import random
import os

# ---------------- Quiz Data ----------------
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": "Paris"
    },
    {
        "question": "Who wrote 'Hamlet'?",
        "options": ["Shakespeare", "Tolstoy", "Hemingway", "Austen"],
        "answer": "Shakespeare"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "What is the largest ocean?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "Pacific"
    },
    {
        "question": "H2O is the chemical formula for?",
        "options": ["Oxygen", "Hydrogen", "Salt", "Water"],
        "answer": "Water"
    },
    {
        "question": "What is 15 + 27?",
        "options": ["42", "43", "45", "41"],
        "answer": "42"
    },
    {
        "question": "Which country is famous for tulips?",
        "options": ["Italy", "Netherlands", "Spain", "Greece"],
        "answer": "Netherlands"
    },
    {
        "question": "Which language is used to create Android apps?",
        "options": ["Python", "Kotlin", "Swift", "JavaScript"],
        "answer": "Kotlin"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Van Gogh", "Picasso", "Da Vinci", "Michelangelo"],
        "answer": "Da Vinci"
    },
    {
        "question": "What does CPU stand for?",
        "options": ["Central Processing Unit", "Control Panel Unit", "Central Panel Unit", "Core Process Unit"],
        "answer": "Central Processing Unit"
    }
]

random.shuffle(questions)

# ---------------- High Score ----------------
def load_high_score():
    if os.path.exists("highscore.json"):
        try:
            with open("highscore.json", "r") as f:
                data = json.load(f)
                if "score" in data and "name" in data:
                    return data
        except json.JSONDecodeError:
            pass
    return {"name": "", "score": 0}

def save_high_score(name, score):
    high = load_high_score()
    if score > high["score"]:
        with open("highscore.json", "w") as f:
            json.dump({"name": name, "score": score}, f)

# ---------------- GUI Application ----------------
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("500x400")
        self.username = tk.simpledialog.askstring("Name", "Enter your name:")

        self.q_index = 0
        self.score = 0
        self.time_left = 30
        self.selected_option = tk.StringVar()
        self.timer_id = None

        self.create_widgets()
        self.load_question()

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="", wraplength=450, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.radio_buttons = []
        for _ in range(4):
            btn = tk.Radiobutton(self.root, text="", variable=self.selected_option, font=("Arial", 12), value="", anchor="w")
            btn.pack(fill="x", padx=40, pady=5)
            self.radio_buttons.append(btn)

        self.timer_label = tk.Label(self.root, text="Time left: 30", font=("Arial", 12, "bold"), fg="red")
        self.timer_label.pack()

        self.next_button = tk.Button(self.root, text="Next", command=self.next_question, bg="blue", fg="white")
        self.next_button.pack(pady=20)

    def load_question(self):
        if self.q_index < len(questions):
            self.selected_option.set(None)
            q = questions[self.q_index]
            self.question_label.config(text=f"Q{self.q_index + 1}: {q['question']}")
            for i, option in enumerate(q["options"]):
                self.radio_buttons[i].config(text=option, value=option)
            self.time_left = 30
            self.update_timer()
        else:
            self.end_quiz()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.next_question(auto=True)

    def next_question(self, auto=False):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        if self.q_index >= len(questions):
            self.end_quiz()
            return

        selected = self.selected_option.get()
        correct = questions[self.q_index]["answer"]

        if not auto and selected == correct:
            self.score += 1

        self.q_index += 1
        if self.q_index < len(questions):
            self.load_question()
        else:
            self.end_quiz()

    def end_quiz(self):
        save_high_score(self.username, self.score)
        high = load_high_score()
        msg = f"Your Score: {self.score}/{len(questions)}\n"
        msg += f"🏆 High Score: {high['score']} by {high['name']}\n"
        if messagebox.askyesno("Quiz Over", msg + "\nDo you want to restart?"):
            self.q_index = 0
            self.score = 0
            random.shuffle(questions)
            self.load_question()
        else:
            self.root.destroy()

# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
