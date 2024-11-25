import time
import random
import string
import tkinter as tk
from tkinter import messagebox
from captcha.image import ImageCaptcha

class CaptchaVerifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CAPTCHA Verifier")
        
        # Set window size
        self.root.geometry("400x300")
        
        self.captcha_text = ""
        self.timestamp = 0
        self.timer_label = None
        
        self.create_widgets()
        self.generate_captcha()

    def create_widgets(self):
        # Increase font size and add padding
        self.captcha_label = tk.Label(self.root, text="CAPTCHA will appear here.", font=("Arial", 16))
        self.captcha_label.pack(pady=20)

        self.captcha_entry = tk.Entry(self.root, font=("Arial", 16), width=20)
        self.captcha_entry.pack(pady=10)

        self.verify_button = tk.Button(self.root, text="Verify CAPTCHA", command=self.verify_captcha, font=("Arial", 14))
        self.verify_button.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        self.message_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.message_label.pack(pady=10)

    def generate_captcha(self):
        self.captcha_text = self.generate_captcha_text()
        self.create_captcha_image(self.captcha_text)
        self.timestamp = time.time()

        # Update the label to show the CAPTCHA text (for demonstration)
        self.captcha_label.config(text=self.captcha_text)

        # Start the countdown timer
        self.start_timer(60)  # 60 seconds

    def generate_captcha_text(self, length=8):  # Increased length for complexity
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))  # Include lowercase letters

    def create_captcha_image(self, captcha_text):
        image = ImageCaptcha()
        image.write(captcha_text, 'captcha.png')

    def start_timer(self, duration):
        self.remaining_time = duration
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            minutes, seconds = divmod(self.remaining_time, 60)
            timer_text = f"Time remaining: {minutes:02}:{seconds:02}"
            self.timer_label.config(text=timer_text)
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)  # Call this method again after 1 second
        else:
            messagebox.showerror("Error", "CAPTCHA expired. Please try again.")
            self.generate_captcha()  # Regenerate CAPTCHA when time expires

    def verify_captcha(self):
        user_input = self.captcha_entry.get()
        current_time = time.time()

        if current_time - self.timestamp > 60:  # Check if more than 1 minute has passed
            messagebox.showerror("Error", "CAPTCHA expired. Please try again.")
            self.generate_captcha()  # Regenerate CAPTCHA
            return

        if user_input == self.captcha_text:
            messagebox.showinfo("Success", "CAPTCHA verified successfully!")
            self.root.destroy()  # Close the application after successful verification
        else:
            messagebox.showerror("Error", "Incorrect CAPTCHA. Please try again.")
            self.generate_captcha()  # Regenerate CAPTCHA after incorrect verification

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaVerifierApp(root)
    root.mainloop()