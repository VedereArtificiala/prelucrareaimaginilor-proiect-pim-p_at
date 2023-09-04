import cv2
import tkinter as tk
from tkinter import Canvas, Scrollbar, VERTICAL
from PIL import Image, ImageTk
from src.recognition import FaceRecognition
import os

class FacialRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recunoaștere Facială")

        self.label1 = tk.Label(root)
        self.label1.pack()

        self.label2 = tk.Label(root)
        self.label2.pack()

        self.capture = cv2.VideoCapture(0)

        self.face_recognition = FaceRecognition("src/known_faces")

        self.capture_button = tk.Button(root, text="Capturează imagine", command=self.capture_image)
        self.capture_button.pack()
        # Actualizează camera și galeria
        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh_camera_and_gallery)
        self.refresh_button.pack()

        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.info_entry = tk.Entry(root)
        self.info_entry.pack()

        self.update()

        # Creează un canvas pentru galerie în fereastra principală
        # Ajustați dimensiunile și stilul galeriei
        self.gallery_canvas = Canvas(root, width=800, height=200)
        self.gallery_canvas.pack()

        # Adaugă o bara de derulare verticală pentru galerie (în cazul în care sunt multe imagini)
        scrollbar = Scrollbar(root, orient=VERTICAL, command=self.gallery_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.gallery_canvas.config(yscrollcommand=scrollbar.set)
        self.gallery_canvas.bind('<Configure>', self.on_canvas_configure)

        # Lista de imagini din directorul proiectului
        self.image_files = [os.path.join("src/known_faces", filename) for filename in os.listdir("src/known_faces")]

        # Afișează galeria
        self.show_gallery()

    def update(self):
        ret, frame = self.capture.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image=img)
            self.label1.img = img
            self.label1.config(image=img)

            names = self.face_recognition.recognize_faces(frame_rgb)
            self.label2.config(text="\n".join(names))

        self.root.after(10, self.update)

    def capture_image(self):
        ret, frame = self.capture.read()
        if ret:
            name = self.name_entry.get()
            img_filename = f"src/known_faces/{name}.jpg"
            cv2.imwrite(img_filename, frame)

    def refresh_camera(self):
        self.capture.release()
        self.capture = cv2.VideoCapture(0)

    def show_gallery(self):
        x = 10
        y = 10
        row_height = 120  # Înălțimea fiecărui rând de imagini
        images_per_row = 5  # Numărul maxim de imagini pe rând

        for i, image_path in enumerate(self.image_files):
            img = Image.open(image_path)
            # Ajustați dimensiunile imaginilor din galerie
            img.thumbnail((100, 100))
            img = ImageTk.PhotoImage(img)
            label = tk.Label(self.gallery_canvas, image=img)
            label.image = img

            # Calculează poziția pe rând și pe coloană pentru fiecare imagine
            row = i // images_per_row
            col = i % images_per_row

            # Afișează imaginea pe canvas la poziția calculată
            label.place(x=col * 120 + x, y=row * row_height + y)

    def on_canvas_configure(self, event):
        self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))

    def refresh_camera_and_gallery(self):
        # Actualizează camera
        self.refresh_camera()

        # Șterge imaginile din galerie existente
        for widget in self.gallery_canvas.winfo_children():
            widget.destroy()

        # Actualizează lista de imagini din directorul proiectului
        self.image_files = [os.path.join("src/known_faces", filename) for filename in os.listdir("src/known_faces")]

        # Afișează galeria actualizată
        self.show_gallery()

if __name__ == "__main__":
    root = tk.Tk()
    app = FacialRecognitionApp(root)
    root.mainloop()
