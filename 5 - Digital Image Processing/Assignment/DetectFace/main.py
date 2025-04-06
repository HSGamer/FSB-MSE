import gradio as gr
import cv2
from face import detect_faces
from dataset import add_new_face, guess_face, load_dataset

# Load the dataset
load_dataset()

def face_recognition(image, threshold):
    image = image.copy()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = detect_faces(image_rgb)
    if faces:
        for (x, y, w, h) in faces:
            face = image_rgb[y:y + h, x:x + w]
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            guess_result = guess_face(face)
            if guess_result is not None:
                name, distance = guess_result
                if distance < threshold:
                    cv2.putText(image, f'{name} {distance:.2f}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return image

def add_face(name, image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    success = add_new_face(name, image_rgb)
    return "Face added successfully!" if success else "Failed to add face."

iface = gr.Blocks()

with iface:
    with gr.Tab("Webcam"):
        with gr.Row():
            with gr.Column():
                webcam_image = gr.Image(label="Input", sources=["webcam"])
            with gr.Column():
                webcam_output = gr.Image(label="Output")
        with gr.Row():
            realtime_threshold_slider = gr.Slider(0.1, 1.0, value=0.6, label="Detection Threshold")
        webcam_image.stream(face_recognition, inputs=[webcam_image, realtime_threshold_slider], outputs=webcam_output, stream_every=0.1)

    with gr.Tab("Image"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(label="Input")
            with gr.Column():
                image_output = gr.Image(label="Output")
        with gr.Row():
            threshold_slider = gr.Slider(0.1, 1.0, value=0.6, label="Detection Threshold")
        gr.Button("Upload").click(face_recognition, inputs=[image_input, threshold_slider], outputs=image_output)

    with gr.Tab("Add Face"):
        name_input = gr.Textbox(label="Name")
        image_input = gr.Image()
        add_face_output = gr.Textbox(label="Status")
        gr.Button("Add").click(add_face, inputs=[name_input, image_input], outputs=add_face_output)

iface.launch()