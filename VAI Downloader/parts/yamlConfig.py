import tkinter as tk
from tkinter import messagebox, filedialog
import yaml
import os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Load config.yaml
def load_config():
    # with open(path + "/config.yaml", 'r') as file:
    #     return yaml.safe_load(file)
    # check if config file exists
    if os.path.exists(path + "/config.yaml"):
        with open(path + "/config.yaml", 'r') as file:
            return yaml.safe_load(file)
    else:
        return {
            'A1111_PATH': '',
            'COLLECTIONURL': '',
            'HEADLESS': False,
            'FILTERTYPE': [],
            'PROFILENAME': '',
            'FIRST_TIME': False
        }

# Save to config.yaml
def save_config(config):
    with open(path + "/config1.yaml", 'w') as file:
        yaml.safe_dump(config, file)

# Update config.yaml with values from the GUI
def update_config():
    config['A1111_PATH'] = entry_a1111_path.get()
    config['COLLECTIONURL'] = entry_collection_url.get()
    config['HEADLESS'] = var_headless.get()
    config['FILTERTYPE'] = [var.get() for var in filter_vars if var.get()]
    config['PROFILENAME'] = entry_profile_name.get()
    config['FIRST_TIME'] = var_first_time.get()
    save_config(config)
    messagebox.showinfo("Success", "Configuration saved successfully!", parent=root)
    root.after(10, root.destroy)  # Automatically close the message box after 0.01 seconds

# Open file dialog to select directory
def select_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        entry_a1111_path.delete(0, tk.END)
        entry_a1111_path.insert(0, selected_directory)

# Load the existing configuration
config = load_config()

# Create the main window
root = tk.Tk()
root.title("Configuration Editor")

# A1111_PATH
tk.Label(root, text="Path to A1111 directory:").grid(row=0, column=0, sticky='w')
entry_a1111_path = tk.Entry(root, width=50)
entry_a1111_path.grid(row=0, column=1)
entry_a1111_path.insert(0, config['A1111_PATH'])
button_browse = tk.Button(root, text="Browse", command=select_directory)
button_browse.grid(row=0, column=2)

# COLLECTIONURL
tk.Label(root, text="Collection URL:").grid(row=1, column=0, sticky='w')
entry_collection_url = tk.Entry(root, width=50)
entry_collection_url.grid(row=1, column=1)
entry_collection_url.insert(0, config['COLLECTIONURL'])

# HEADLESS
tk.Label(root, text="Run in headless mode:").grid(row=2, column=0, sticky='w')
var_headless = tk.BooleanVar()
var_headless.set(config['HEADLESS'])
tk.Checkbutton(root, variable=var_headless).grid(row=2, column=1, sticky='w')

# FILTERTYPE
tk.Label(root, text="Filter types:").grid(row=3, column=0, sticky='w')
filter_types = ["lora", "lycoris", "checkpoint", "hypernetwork", "embedding"]
filter_vars = []
row = 3
for filter_type in filter_types:
    var = tk.StringVar()
    if filter_type in config['FILTERTYPE']:
        var.set(filter_type)
    else:
        var.set("")
    filter_vars.append(var)
    tk.Checkbutton(root, text=filter_type, variable=var, onvalue=filter_type, offvalue="").grid(row=row, column=1, sticky='w')
    row += 1

# PROFILENAME
tk.Label(root, text="Profile name:").grid(row=row, column=0, sticky='w')
entry_profile_name = tk.Entry(root, width=50)
entry_profile_name.grid(row=row, column=1)
entry_profile_name.insert(0, config['PROFILENAME'])

# FIRST_TIME
row += 1
tk.Label(root, text="First time run:").grid(row=row, column=0, sticky='w')
var_first_time = tk.BooleanVar()
var_first_time.set(config['FIRST_TIME'])
tk.Checkbutton(root, variable=var_first_time).grid(row=row, column=1, sticky='w')

# Save button
row += 1
tk.Button(root, text="Save", command=update_config).grid(row=row, columnspan=2)

# Run the application
root.mainloop()