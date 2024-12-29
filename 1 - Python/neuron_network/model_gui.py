import tensorflow as tf
import tkinter as tk
import cv2
from util import img_to_sample

model = tf.keras.models.load_model("model.keras")

app = tk.Tk()
app.title("Digit Recognizer")
app.geometry("500x500")

label = tk.Label(app, text="Select an image")
label.pack()

prediction = tk.StringVar()

def open_image():
    from tkinter import filedialog
    filename = filedialog.askopenfilename()
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    image = img_to_sample(image)
    image = image.reshape(1, 128, 128, 1)
    prediction.set(model.predict(image).argmax())

button = tk.Button(app, text="Open Image", command=open_image)
button.pack()

label = tk.Label(app, text="Prediction")
label.pack()

label = tk.Label(app, textvariable=prediction)
label.pack()

app.mainloop()