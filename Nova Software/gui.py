# import tkinter as tk
# from tkinter import Label
# from PIL import Image, ImageTk

# def open_gui():
#     root = tk.Tk()

#     # Calculate the screen width and height
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
def search_title

#     # Set the GUI window size and position it at the center of the screen
#     window_width = 800
#     window_height = 600
#     x_coordinate = (screen_width - window_width) // 2
#     y_coordinate = (screen_height - window_height) // 2

#     root.title("My GUI")
#     root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
#     root.configure(bg="black")

#     # Load the GIF image
#     gif_image = Image.open("images/player.gif")
#     gif_photo = ImageTk.PhotoImage(gif_image)

#     # Create a Label widget to display the GIF
#     label = Label(root, image=gif_photo, bg="black")
#     label.place(relx=0.5, rely=0.5, anchor="center")

#     # Start the loop to continuously display the GIF
#     label.after(0, lambda: loop_gif(label, gif_image))

#     root.mainloop()

# def loop_gif(label, gif_image):
#     # This function loops the GIF animation
#     label.configure(image=gif_image)
#     label.image = gif_image
#     label.after(100, lambda: loop_gif(label, gif_image))

# if __name__ == "__main__":
#     open_gui()

import tkinter as tk
from PIL import Image, ImageTk

class AnimatedGIFLabel(tk.Label):
    def __init__(self, master, path_to_gif):
        self.path_to_gif = path_to_gif
        self.frames = []
        self.idx = 0
        self.delay = 100  # Adjust the delay as needed
        self.load_frames()
        super().__init__(master)

    def load_frames(self):
        gif = Image.open(self.path_to_gif)
        try:
            while True:
                gif.seek(gif.tell() + 1)
                self.frames.append(ImageTk.PhotoImage(gif.copy()))
        except EOFError:
            pass

    def animate(self):
        self.config(image=self.frames[self.idx])
        self.idx = (self.idx + 1) % len(self.frames)
        self.after(self.delay, self.animate)

def open_gui():
    root = tk.Tk()

    # Calculate the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the GUI window size and position it at the center of the screen
    window_width = 800
    window_height = 600
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2

    root.title("My GUI")
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    root.configure(bg="black")

    # Create an instance of AnimatedGIFLabel to display the GIF
    gif_label = AnimatedGIFLabel(root, "images/player.gif")
    gif_label.place(relx=0.5, rely=0.5, anchor="center")
    gif_label.animate()

    root.mainloop()

if __name__ == "__main__":
    open_gui()

