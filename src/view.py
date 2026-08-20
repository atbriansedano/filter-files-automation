import customtkinter as ctk
from tkinter import messagebox
from main import get_file_paths, move_files
from pathlib import Path
import json
import os

APP_DATA_DIR = os.path.join(os.environ["APPDATA"], "FileAutomation")
os.makedirs(APP_DATA_DIR, exist_ok=True)
SAVE_FILE = os.path.join(APP_DATA_DIR, "monitored_paths.json")

# Initializing monitoring paths
monitored_paths = []

# Two alternating colors for rows
ROW_COLOR_1 = "#2b2b2b"
ROW_COLOR_2 = "#565353"

def save_paths():
    with open(SAVE_FILE, "w") as f:
        json.dump(monitored_paths, f)

def load_paths():
    if not os.path.exists(SAVE_FILE):
        return []
    with open(SAVE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def create_row(path_entry):
    row_index = len(monitored_paths) - 1
    color = ROW_COLOR_1 if row_index % 2 == 0 else ROW_COLOR_2

    row_frame = ctk.CTkFrame(path_list, fg_color=color, corner_radius=4)
    row_frame.pack(fill="x", padx=5, pady=1)

    row_label = ctk.CTkLabel(row_frame, text=path_entry, anchor="w", fg_color="transparent")
    row_label.pack(side="left", fill="x", expand=True, padx=5, pady=2)

    delete_button = ctk.CTkButton(
        row_frame, text="✕", width=28,
        fg_color="#8b3a3a", hover_color="#a94444",
        command=lambda: delete_path(path_entry, row_frame)
    )
    delete_button.pack(side="right", padx=5)

def add_path():
    path_entry = path_box.get()
    if path_entry.strip() == '':
        return
    monitored_paths.append(path_entry)
    create_row(path_entry)
    save_paths()
    path_box.delete(0, "end")

def delete_path(path_entry, row_frame):
    if path_entry in monitored_paths:
        monitored_paths.remove(path_entry)
    row_frame.destroy()
    save_paths()

def execute_action():
    if not monitored_paths:
        messagebox.showwarning("No paths", "Add at least one folder to monitor first.")
        return

    move_to_path = Path.home() / "Documents/File Automation"

    try:
        file_paths = get_file_paths(monitored_paths)
        move_files(file_paths, move_to_path, is_date_subfolder=True, is_extension_subfolder=True)
        messagebox.showinfo("Done", f"Moved {len(file_paths)} file(s) to {move_to_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_closing():
    save_paths()
    app.destroy()

# Create the main window
app = ctk.CTk()
app.geometry("800x300")

# View
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=10, pady=10)

path_box = ctk.CTkEntry(input_frame, placeholder_text="Enter folder path...")
path_box.pack(side="left", fill="x", expand=True, padx=(0, 5))

add_path_button = ctk.CTkButton(input_frame, text="→", width=40, command=add_path)
add_path_button.pack(side="left")

# --- Execute button at the bottom ---
execute_button = ctk.CTkButton(app, text="Execute", command=execute_action)
execute_button.pack(side="bottom", pady=10)

# --- Display box below ---
path_list = ctk.CTkScrollableFrame(app, label_text="Saved Paths")
path_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

# Load saved paths and rebuild rows on startup
for saved_path in load_paths():
    monitored_paths.append(saved_path)
    create_row(saved_path)

# Save automatically when the window is closed
app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()