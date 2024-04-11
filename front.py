import tkinter as tk
import threading
import speech_recognition as sr

class TranslatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Speech Translator")

        self.translated_text = tk.StringVar()
        self.input_audio_text = tk.StringVar()

        self.label_input_audio = tk.Label(master, text="Input Audio:")
        self.label_input_audio.pack()

        self.input_audio_textbox = tk.Text(master, height=5, width=50)
        self.input_audio_textbox.pack()

        self.label_translated_text = tk.Label(master, text="Translated Text:")
        self.label_translated_text.pack()

        self.translated_textbox = tk.Text(master, height=5, width=50)
        self.translated_textbox.pack()

        # Load the images for start and stop buttons
        self.start_img = tk.PhotoImage(file="start_button.png").subsample(3)
        self.stop_img = tk.PhotoImage(file="stop_button.png").subsample(5)

        # Create the start button with a green triangle image
        self.listen_button = tk.Button(master, image=self.start_img, command=self.start_listening, bd=0, highlightthickness=0)
        self.listen_button.pack(side=tk.LEFT)

        # Create the stop button with a red square image
        self.stop_button = tk.Button(master, image=self.stop_img, command=self.stop_listening, bd=0, highlightthickness=0, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)

        self.is_listening = False

    def start_listening(self):
        # Disable the start button and enable the stop button
        self.listen_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start a new thread for listening to microphone input
        self.is_listening = True
        threading.Thread(target=self.listen_and_translate).start()

    def stop_listening(self):
        # Set the flag to stop listening
        self.is_listening = False

        # Disable the stop button and enable the start button
        self.listen_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def listen_and_translate(self):
        # Function to start listening to microphone input
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            while self.is_listening:
                audio = r.listen(source)
                try:
                    print("Recognizing...")
                    text = r.recognize_google(audio)
                    self.input_audio_textbox.delete("1.0", tk.END)
                    self.input_audio_textbox.insert(tk.END, text)
                    # Here you can call your backend function to translate 'text'
                    translated_text = "Translated: " + text  # Placeholder translation
                    self.translated_textbox.delete("1.0", tk.END)
                    self.translated_textbox.insert(tk.END, translated_text)
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))

root = tk.Tk()
app = TranslatorApp(root)
root.mainloop()
