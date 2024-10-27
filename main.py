import sys

from PIL import Image, ImageTk
import tkinter as tk
import os


class DesktopPet:
    def __init__(self, root, gif_path):
        self.root = root
        self.root.overrideredirect(True)  # Remove window borders
        self.root.wm_attributes("-topmost", 1)  # Keep window always on top
        self.root.wm_attributes("-transparentcolor", "white")  # Make white color transparent

        self.width = 150
        self.height = 150
        self.y_position = root.winfo_screenheight() - self.height - 40  # Change this value as needed

        self.root.geometry(
            f"{self.width}x{self.height}+0+{self.y_position}")  # Place the canvas at specified y position

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white", highlightthickness=0)
        self.canvas.pack()

        # Load the pet GIF and extract frames
        if not os.path.exists(gif_path):
            raise FileNotFoundError(f"File {gif_path} not found.")

        # Initial movement settings
        self.x_move = 1
        self.y_move = 0
        self.flip = False  # Variable to track flip state

        self.frames = self.load_gif_frames(gif_path)

        # Create initial image on the canvas
        self.image_id = self.canvas.create_image(self.width / 2, self.height / 2, image=self.frames[0])

        self.current_frame = 0
        self.update_frame()

        # Start moving the pet
        self.move_pet()

        # Bind left mouse click to close the pet
        self.root.bind("<Button-1>", self.quit)

    def load_gif_frames(self, gif_path):
        """Load all frames from a GIF file and create flipped versions."""
        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                # Append the current frame to the list
                frame = gif.copy().convert("RGBA")  # Ensure the image has the correct format
                frames.append(ImageTk.PhotoImage(frame))  # Normal frame
                # Append the mirrored frame
                mirrored_frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
                frames.append(ImageTk.PhotoImage(mirrored_frame))  # Flipped frame
                gif.seek(gif.tell() + 1)  # Go to the next frame
        except EOFError:
            pass  # End of GIF
        return frames

    def update_frame(self):
        # Loop through the frames of the pet GIF
        self.current_frame = (self.current_frame + 1) % (len(self.frames) // 2)  # Only iterate through normal frames
        # Determine the correct frame based on the flip state
        if self.flip:
            frame_index = self.current_frame * 2 + 1  # Flipped frame
        else:
            frame_index = self.current_frame * 2  # Normal frame
        self.canvas.itemconfig(self.image_id, image=self.frames[frame_index])
        self.root.after(100, self.update_frame)  # Update frame every 100ms

    def move_pet(self):
        # Get the current position of the window
        x, y = self.root.winfo_x(), self.y_position

        # Move the window by x_move and y_move
        new_x = x + self.x_move
        new_y = y + self.y_move
        self.root.geometry(f"+{new_x}+{new_y}")

        # Get the width and height of the window
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Check if the pet hits the screen boundaries and change direction
        if new_x <= 0:  # Left boundary
            self.x_move = abs(self.x_move)  # Move right
            self.flip = False  # Flip to normal
        elif new_x + window_width >= self.root.winfo_screenwidth():  # Right boundary
            self.x_move = -abs(self.x_move)  # Move left
            self.flip = True  # Flip to mirrored

        if new_y <= 0:  # Top boundary
            self.y_move = abs(self.y_move)  # Move down
        elif new_y + window_height >= self.root.winfo_screenheight():  # Bottom boundary
            self.y_move = -abs(self.y_move)  # Move up

        self.root.after(5, self.move_pet)  # Repeat movement every 50ms

    def quit(self, event):
        self.root.destroy()


# Main function to run the pet
if __name__ == "__main__":
    root = tk.Tk()
    # Get the directory of the running script or executable
    if getattr(sys, 'frozen', False):
        # If the program is running as an executable
        base_path = sys._MEIPASS  # This is the temporary folder where PyInstaller extracts the files
    else:
        # If the program is running in a regular Python environment
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to duck.gif
    gif_path = os.path.join(base_path, "duck.gif")
    pet = DesktopPet(root, gif_path)
    root.mainloop()
