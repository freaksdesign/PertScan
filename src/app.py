import os
import tkinter as tk
from src import resource_dir
from src.main import MainView


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)

    root.title("Port Scanner")
    root.iconbitmap(os.path.join(resource_dir, "icon.ico"))
    root.wm_geometry("720x480")
    root.resizable(False, False)

    root.config(menu=main.menubar)

    root.mainloop()
