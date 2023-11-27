import tkinter as tk
from src.app import App  # Adjust import path

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
