import tkinter as tk
from src.gui import FacialRecognitionApp

if __name__ == "__main__":
    root = tk.Tk()
    app = FacialRecognitionApp(root)
    root.mainloop()
