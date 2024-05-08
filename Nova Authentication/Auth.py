import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk


class HandSignCaptureGUI:

    hand_auth = []

    def __init__(self, master, num_frames=60):
        self.master = master
        self.num_frames = num_frames

        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        self.canvas = tk.Canvas(master, width=640, height=480)
        self.canvas.pack()

        self.btn_capture = tk.Button(
            master, text="Store Authentication Sign", command=self.store_hand
        )
        self.btn_capture.pack()

        self.btn_compare = tk.Button(
            master,
            text="Check Authentication Match",
            command=lambda: self.compare_hand_sign(self.hand_auth, self.get_hand()),
        )
        self.btn_compare.pack()

        self.update_camera_feed()

    def store_hand(self):
        self.hand_auth = self.capture_hand_sign()
        print("Auth Hand Stored")

    def get_hand(self):
        hand = self.capture_hand_sign()
        if hand:
            print("Hand Captured")
            return hand

    def update_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for landmark in hand_landmarks.landmark:
                        x, y = int(landmark.x * frame.shape[1]), int(
                            landmark.y * frame.shape[0]
                        )
                        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk  # Keep reference to avoid garbage collection
            self.master.after(
                10, self.update_camera_feed
            )  # Update every 10 milliseconds
        else:
            print("Error: Failed to capture frame.")

    def capture_hand_sign(self):
        hand_sign = []

        for _ in range(self.num_frames):
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for landmark in hand_landmarks.landmark:
                        x, y = int(landmark.x * frame.shape[1]), int(
                            landmark.y * frame.shape[0]
                        )
                        hand_sign.append((x, y))
        return hand_sign

    def compare_hand_sign(self, sign1, sign2, tolerance=20):
        if len(sign1) != len(sign2):
            print("No Match")
            return False

        # Check if the distance between each pair of points is within tolerance
        for point1, point2 in zip(sign1, sign2):
            if (
                abs(point1[0] - point2[0]) > tolerance
                or abs(point1[1] - point2[1]) > tolerance
            ):
                print("No Match")
                return False

        print("Match")
        return True


def main():
    root = tk.Tk()
    root.title("Hand Sign Capture")
    app = HandSignCaptureGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
