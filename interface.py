
import tkinter as tk
from tkinter import ttk

import threading
import pybullet as p
import time
import pybullet_data


from multiprocessing import Process, Array

#from visualisation import main as pybullet_main


def run_pybullet_simulation():
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)

    # Load the Puma 560 URDF
    robot_id = p.loadURDF("./puma560_robot.urdf", [0, 0, 0.1])

    while True:
        p.stepSimulation()
        time.sleep(1. / 240.)

# Add your callback functions here
def button_1_clicked():
    print("Button 1 clicked")

def button_2_clicked():
    print("Button 2 clicked")

def slider_updated(value):
    print(f"Slider updated: {value}")



def on_serial_enter(event, input_text, history_text):
    command = input_text.get("1.0", tk.END).strip()
    print(f"Serial input: {command}")

    history_text.tag_configure("user_input", foreground="red")
    history_text.tag_configure("command_result", foreground="blue")

    # Add the command to the history text widget
    history_text.insert(tk.END, f"{command}\n", "user_input")
    

    # Simulate a command result (replace this with actual command handling)
    command_result = "Command successful"
    # Add the command result to the history text widget with the "command_result" tag
    history_text.insert(tk.END, f"{command_result}\n", "command_result")
    history_text.see(tk.END)  # Scroll to the end


    # Clear the input text widget
    input_text.delete("1.0", tk.END)

def set_dark_theme(root):
    dark_bg = "#424242"
    dark_fg = "#ffffff"
    dark_accent = "#00bcd4"

    root.configure(bg=dark_bg)

    style = ttk.Style(root)
    style.theme_use("default")

    style.configure("TFrame", background=dark_bg)
    style.configure("TButton", background=dark_bg, foreground=dark_fg)
    style.configure("TLabel", background=dark_bg, foreground=dark_fg)
    style.configure("TScale", background=dark_bg, foreground=dark_fg, troughcolor=dark_accent)
    style.configure("Vertical.TScrollbar", background=dark_bg, troughcolor=dark_accent)


def main():
    root = tk.Tk()
    root.title("Robot Control GUI")


    # Set the dark theme
    set_dark_theme(root)


    # Create a container for the three top panels
    top_frame = ttk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create a left panel with sliders
    left_frame = ttk.Frame(top_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

    slider_1 = ttk.Scale(left_frame, from_=0, to=180, orient=tk.VERTICAL)
    slider_1.pack(side=tk.LEFT, padx=5)
    slider_2 = ttk.Scale(left_frame, from_=0, to=180, orient=tk.VERTICAL)
    slider_2.pack(side=tk.LEFT, padx=5)

    # Create a center panel
    center_frame = ttk.Frame(top_frame)
    center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Create a right panel with buttons
    right_frame = ttk.Frame(top_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)

    button_1 = ttk.Button(right_frame, text="Button 1")
    button_1.pack(pady=5)
    button_2 = ttk.Button(right_frame, text="Button 2")
    button_2.pack(pady=5)

    # Create a bottom frame for the serial subwindow
    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5)

    # Create a frame for the serial history and input widgets
    serial_frame = ttk.Frame(bottom_frame)
    serial_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a frame for the serial history and input widgets
    serial_frame = ttk.Frame(bottom_frame)
    serial_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a text widget for the serial history
    history_text = tk.Text(serial_frame, wrap=tk.NONE, height=10)
    history_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create a text widget for the serial input
    input_text = tk.Text(serial_frame, wrap=tk.NONE, height=1)
    input_text.pack(side=tk.BOTTOM, fill=tk.X)

    # Bind the Return key in the input text widget to the callback function
    input_text.bind("<Return>", lambda event, i=input_text, h=history_text: on_serial_enter(event, i, h))


    # Bind the buttons to their callback functions
    button_1.config(command=button_1_clicked)
    button_2.config(command=button_2_clicked)

    # Bind the sliders to the callback function
    slider_1.config(command=lambda value=slider_1.get(): slider_updated(value))
    slider_2.config(command=lambda value=slider_2.get(): slider_updated(value))

    # Bind the Return key in the serial window to the callback function
    #serial_text.bind("<Return>", lambda event, s=serial_text: on_serial_enter(event, s))
    
    # Start the PyBullet simulation in a separate thread
    simulation_thread = threading.Thread(target=run_pybullet_simulation, daemon=True)
    simulation_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()