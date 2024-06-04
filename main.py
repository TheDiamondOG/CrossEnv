import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox


def add_env_var(name: str, value: str, local: bool = False):
    if local:
        os.environ[name] = value
    else:
        if os.name == "nt":
            subprocess.run(["setx", name, value])
        else:
            try:
                # Open the file in append mode and add your variable
                with open("/etc/environment", "a") as env_file:
                    env_file.write(f"{name}={value}\n")
            except Exception as e:
                return e
    return f"{name}={value}"


def os_key_grabber():
    data_list = []
    for key, value in os.environ.items():
        data_var = {"key": key, "value": value}
        data_list.append(data_var)
    return data_list


class EnvVarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CrossEnv")

        self.style = ttk.Style()

        self.dark_mode = tk.BooleanVar()
        self.dark_mode.set(False)

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tree = ttk.Treeview(self.main_frame, columns=("name", "value"), show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("value", text="Value")
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tree.bind("<Double-1>", self.on_double_click)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.add_frame = ttk.Frame(self.main_frame, padding="5")
        self.add_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Label(self.add_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(self.add_frame, text="Value:").grid(row=1, column=0, sticky=tk.W)
        self.value_entry = ttk.Entry(self.add_frame)
        self.value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        self.local_var = tk.BooleanVar()
        self.local_check = ttk.Checkbutton(self.add_frame, text="Local", variable=self.local_var)
        self.local_check.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        self.add_button = ttk.Button(self.add_frame, text="Add Variable", command=self.add_variable)
        self.add_button.grid(row=3, column=0, columnspan=2)
        self.toggle_button = ttk.Button(self.main_frame, text="Dark Mode", command=self.toggle_dark_mode)
        self.toggle_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.populate_tree()
        self.apply_theme()

    def populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data_list = os_key_grabber()
        for data in data_list:
            self.tree.insert("", tk.END, values=(data["key"], data["value"]))

    def add_variable(self):
        name = self.name_entry.get()
        value = self.value_entry.get()
        local = self.local_var.get()

        if not name or not value:
            messagebox.showerror("Error", "Both Name and Value is needed")
            return

        result = add_env_var(name, value, local)
        if isinstance(result, Exception):
            messagebox.showerror("Error", str(result))
        else:
            messagebox.showinfo("Success", f"Added {result}")
            self.populate_tree()

    def toggle_dark_mode(self):
        self.dark_mode.set(not self.dark_mode.get())
        self.apply_theme()
        if self.dark_mode.get():
            self.toggle_button.config(text="Light Mode")
        else:
            self.toggle_button.config(text="Dark Mode")

    def apply_theme(self):
        if self.dark_mode.get():
            self.style.configure("TFrame", background="#2e2e2e")
            self.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
            self.style.configure("TEntry", fieldbackground="#4d4d4d", foreground="#ffffff")
            self.style.configure("TButton", background="#3c3c3c", foreground="#ffffff")
            self.style.configure("Treeview", background="#3c3c3c", foreground="#ffffff", fieldbackground="#3c3c3c")
            self.style.configure("Treeview.Heading", background="#4d4d4d", foreground="#ffffff")
            self.style.configure("Vertical.TScrollbar", troughcolor="#3c3c3c", background="#4d4d4d",
                                 arrowcolor="#ffffff")

            # Button hover effect
            self.style.map("TButton",
                           background=[("active", "#555555")],
                           foreground=[("active", "#ffffff")])

            # Configure Checkbutton for dark mode
            self.style.configure("TCheckbutton", background="#2e2e2e", foreground="#ffffff")
            self.style.map("TCheckbutton",
                           background=[("active", "#555555"), ("selected", "#3c3c3c")],
                           foreground=[("active", "#ffffff"), ("selected", "#ffffff")])
        else:
            self.style.configure("TFrame", background="#f0f0f0")
            self.style.configure("TLabel", background="#f0f0f0", foreground="#000000")
            self.style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")
            self.style.configure("TButton", background="#e0e0e0", foreground="#000000")
            self.style.configure("Treeview", background="#ffffff", foreground="#000000", fieldbackground="#ffffff")
            self.style.configure("Treeview.Heading", background="#e0e0e0", foreground="#000000")
            self.style.configure("Vertical.TScrollbar", troughcolor="#e0e0e0", background="#c0c0c0",
                                 arrowcolor="#000000")

            # Remove button hover effect
            self.style.map("TButton",
                           background=[("active", "#d9d9d9")],
                           foreground=[("active", "#000000")])

            # Configure Checkbutton for light mode
            self.style.configure("TCheckbutton", background="#f0f0f0", foreground="#000000")
            self.style.map("TCheckbutton",
                           background=[("active", "#d9d9d9"), ("selected", "#e0e0e0")],
                           foreground=[("active", "#000000"), ("selected", "#000000")])

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)

        col = int(column.replace('#', '')) - 1
        x, y, width, height = self.tree.bbox(item, column)

        entry = ttk.Entry(self.main_frame)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, self.tree.item(item, "values")[col])

        entry.bind("<FocusOut>", lambda e: self.on_edit(item, col, entry))
        entry.bind("<Return>", lambda e: self.on_edit(item, col, entry, True))
        entry.focus_set()

    def on_edit(self, item, col, entry, update=False):
        if update:
            new_value = entry.get()
            values = list(self.tree.item(item, "values"))
            old_name = values[0]
            values[col] = new_value
            self.tree.item(item, values=values)
            if col == 0:
                self.update_env_var(old_name, values[0], values[1], True)
            else:
                self.update_env_var(values[0], values[1])

        entry.destroy()

    def update_env_var(self, old_name, name, value, name_changed=False):
        if os.name == "nt":
            if name_changed:
                # Delete the old variable
                subprocess.run(["setx", old_name, ""])
            # Add the new variable
            subprocess.run(["setx", name, value])
        else:
            with open("/etc/environment", "r") as file:
                lines = file.readlines()
            with open("/etc/environment", "w") as file:
                for line in lines:
                    if line.startswith(old_name + "="):
                        file.write(f"{name}={value}\n")
                    else:
                        file.write(line)
        os.environ.pop(old_name, None)
        os.environ[name] = value


if __name__ == "__main__":
    root = tk.Tk()
    app = EnvVarApp(root)
    root.mainloop()
