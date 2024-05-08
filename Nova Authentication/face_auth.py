import cv2
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import face_recognition
from cryptography.fernet import Fernet
import os


class FaceAuthentication:

    def store_face(self):
        key = self.encryption_key()
        while True:
            try:
                # Create camera and capture face image
                face_image = self.create_camera()

                # Convert face_image to bytes
                face_image_bytes = cv2.imencode(".jpg", face_image)[1].tobytes()

                # Encrypt the face image
                cipher_suite = Fernet(key)
                encrypted_face_image = cipher_suite.encrypt(face_image_bytes)

                # Store the encrypted face image into face.bin
                with open("face.bin", "wb") as encrypted_file:
                    encrypted_file.write(encrypted_face_image)

                return f"Face stored successfully."
            except Exception as e:
                print(f"Error storing face: {e}")
                continue

    def compare_face(self):
        key = self.encryption_key()
        while True:
            try:
                # Capture a new face image
                new_face_image = self.create_camera()

                # Load the stored encrypted face image
                with open("face.bin", "rb") as encrypted_file:
                    encrypted_face_image = encrypted_file.read()

                # Decrypt the stored face image
                cipher_suite = Fernet(key)
                decrypted_face_image = cipher_suite.decrypt(encrypted_face_image)

                # Convert the decrypted face image back to numpy array
                nparr = np.frombuffer(decrypted_face_image, np.uint8)
                stored_face_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Convert the new face image to RGB format
                new_face_image_rgb = cv2.cvtColor(new_face_image, cv2.COLOR_BGR2RGB)

                # Detect face encodings for both images
                new_face_encodings = face_recognition.face_encodings(new_face_image_rgb)
                stored_face_encodings = face_recognition.face_encodings(
                    stored_face_image
                )

                # Ensure that both images contain faces
                if len(new_face_encodings) > 0 and len(stored_face_encodings) > 0:
                    # Compare face encodings
                    results = face_recognition.compare_faces(
                        stored_face_encodings, new_face_encodings[0]
                    )

                    # Determine if a match is found
                    if results[0]:
                        return "Face match found."

            except Exception as e:
                print(f"Error comparing faces: {e}")
                continue

    def create_camera(self):
        self.root = Tk()
        self.cap = cv2.VideoCapture(0)
        self.canvas = Canvas(self.root, width=640, height=480)
        self.root.title("Face Capture")
        self.canvas.pack()

        face_locations, frame = self.update_camera()  # Initial call to update_camera
        top, right, bottom, left = face_locations[0]

        # Extract the face region
        face_image = frame[top:bottom, left:right]

        self.cap.release()  # Release the video capture object
        cv2.destroyAllWindows()  # Close any OpenCV windows
        self.root.destroy()

        return face_image

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert frame to RGB for face_recognition library
            rgb_frame = frame[:, :, ::-1]

            # Find all face locations in the current frame
            face_locations = face_recognition.face_locations(rgb_frame)

            # Loop through each face found in the frame
            for top, right, bottom, left in face_locations:
                # Draw a rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Find all facial landmarks in the current face
                landmarks = face_recognition.face_landmarks(
                    rgb_frame, [(top, right, bottom, left)]
                )[0]

                # Loop through each facial landmark and draw a circle
                for landmark_type, landmarks_list in landmarks.items():
                    for landmark in landmarks_list:
                        cv2.circle(frame, landmark, 2, (255, 0, 0), -1)

            # Convert the frame back to BGR before displaying
            cv2image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Convert BGR image to PIL format
            img = Image.fromarray(cv2image)

            # Convert PIL image to Tkinter PhotoImage
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the canvas with the new image
            self.canvas.imgtk = imgtk  # Keep a reference to avoid garbage collection
            self.canvas.create_image(0, 0, anchor=NW, image=imgtk)

            # If a face is detected
            if face_locations:
                return face_locations, frame
            else:
                # Call update_camera again after a delay (adjust as needed)
                self.root.after(10, self.update_camera)

    def encryption_key(self):
        file = "encryption_key.txt"
        if os.path.exists(file):
            with open(file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(file, "wb") as f:
                f.write(key)
            return key


if __name__ == "__main__":
    face_auth = FaceAuthentication()
    face_auth.encryption_key()
