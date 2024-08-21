import tkinter as tk
from customtkinter import *

def redshadowbox(message):
    root = CTk()
    root.overrideredirect(True)    
    temp_label = tk.Label(root, text=message, font=("Arial", 15, "bold"))
    temp_label.update_idletasks()
    text_width = temp_label.winfo_reqwidth()
    window_width = text_width + 10
    window_height = 120

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    
    frame_alart = CTkFrame(root)
    frame_alart.pack(fill="both", expand=True, padx=5, pady=5)

    label = CTkLabel(frame_alart, text=message, padx=5, pady=5, fg_color="#323232", bg_color="#333333", font=("Arial", 15, "bold"), wraplength=window_width-20)
    label.pack(pady=(10, 10))
    
    button = CTkButton(frame_alart, text="OK", command=root.destroy, fg_color="#212121", hover_color="#323232")
    button.pack(pady=(0, 0))
    
    root.mainloop()