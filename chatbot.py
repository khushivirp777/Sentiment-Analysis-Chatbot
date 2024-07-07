from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, Frame, ttk
from textblob import TextBlob
import nltk
import random

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    from textblob.download_corpora import main
    main()
except nltk.exceptions.ContentRetrievalError:
    print("Error downloading corpora. Please check your internet connection.")

class ChatbotApp:
    def __init__(self, master):
        self.master = master
        master.title("Sentiment Analysis Chatbot")

        self.frame = Frame(master, padx=20, pady=20)
        self.frame.pack()

        self.label = ttk.Label(self.frame, text="Enter text:", font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, sticky='w')

        self.entry = ttk.Entry(self.frame, width=40, font=("Arial", 12))
        self.entry.grid(row=1, column=0, padx=5, pady=5)

        self.button = ttk.Button(self.frame, text="Analyze", command=self.analyze_text, style="Accent.TButton")
        self.button.grid(row=2, column=0, pady=10)

        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.reset_text, style="Danger.TButton")
        self.reset_button.grid(row=2, column=1, padx=5)

        self.output_text = Text(self.frame, wrap='word', height=10, width=50, state='disabled', font=("Arial", 12))
        self.output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.scrollbar = Scrollbar(self.frame, command=self.output_text.yview)
        self.scrollbar.grid(row=3, column=2, sticky='ns')

        self.output_text.config(yscrollcommand=self.scrollbar.set)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Accent.TButton", foreground="green", background="white")
        self.style.configure("Danger.TButton", foreground="red", background="white")

    def fade_in(self, widget, alpha):
        widget.attributes("-alpha", alpha)
        alpha += 0.1
        if alpha <= 1.0:
            self.master.after(50, self.fade_in, widget, alpha)

    def display_analysis_result(self, output_message):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, END)
        self.output_text.insert(END, output_message + '\n\n')
        self.output_text.config(state='disabled')

        # Fade-in animation
        self.master.after(50, self.fade_in, self.output_text, 0.0)

    def analyze_text(self):
        user_input = self.entry.get()

        sentiment, polarity, subjectivity, analysis = self.analyze_sentiment(user_input)
        explanation = self.generate_explanation(sentiment, polarity, subjectivity)
        output_message = f"Sentiment: {sentiment}\nPolarity: {polarity:.2f}\nSubjectivity: {subjectivity:.2f}\n\nExplanation: {explanation}"

        self.display_analysis_result(output_message)
        self.entry.delete(0, 'end')

    def reset_text(self):
        self.entry.delete(0, 'end')
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, END)
        self.output_text.config(state='disabled')

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        polarity, subjectivity = analysis.sentiment.polarity, analysis.sentiment.subjectivity
        sentiment = 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'
        return sentiment, polarity, subjectivity, analysis

    def generate_explanation(self, sentiment, polarity, subjectivity):
        explanation = f"The sentiment of the text is {sentiment.lower()}. "
        explanation += (
            f"It generally expresses a {'positive' if sentiment == 'Positive' else 'negative' if sentiment == 'Negative' else 'neutral'} opinion or emotion. "
            f"The polarity score is {polarity:.2f}, where a higher value indicates a stronger sentiment. "
            f"The subjectivity score is {subjectivity:.2f}, where a higher value indicates more subjective content."
        )
        return explanation

    def show_quote(self):
        quotes = [
            "“Believe you can and you're halfway there.” - Theodore Roosevelt",
            "“The only way to do great work is to love what you do.” - Steve Jobs",
            "“It does not matter how slowly you go as long as you do not stop.” -Confucius",
            "“Success is not final, failure is not fatal: It is the courage to continue that counts.” - Winston Churchill",
            "“Don't watch the clock; do what it does. Keep going.” - Sam Levenson"
        ]
        quote_label = Label(self.frame, text=random.choice(quotes), wraplength=400, font=("Arial", 12, "italic"))
        quote_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.master.after(10000, quote_label.destroy)

    def start_quote_timer(self):
        self.show_quote()
        self.master.after(10000, self.start_quote_timer)

if __name__ == "__main__":
    root = Tk()
    app = ChatbotApp(root)
    app.start_quote_timer()
    root.mainloop()