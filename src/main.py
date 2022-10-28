__all__ = ['Page', 'Page1', 'Page2', 'MainView']

# Import Libs
import os
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from src import img_dir

import socket
import threading
from queue import Queue


# Default Page (structure that each Page inherits)
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        """ ====================
             PAGE CONFIGURATION
            ==================== """
        # Set the default fonts
        self.small_font = font.Font(self, family="Cambria", size=12)
        self.medium_font = font.Font(self, family="Cambria", size=14)
        self.large_font = font.Font(self, family="Cambria", size=16)
        self.title_font = font.Font(self, family="Tw Cen MT Condensed", size=18, weight="bold")

    """ Method to lift a page to the topmost "layer" (to view a page) """
    def show(self):
        # Raise page to the top of the "stack" of pages
        self.lift()


# Page 1
class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        """ ========================
             INITIALIZE VARIABLE(S)
            ======================== """
        # ...

        """ ====================
             PAGE CONFIGURATION
            ==================== """
        self.scan_button = tk.Button(self, text="Scan", font=self.medium_font)
        self.scan_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Result table
        result_columns = ('ip', 'port_num', 'port_status', 'port_name', 'description')
        self.scan_results = ttk.Treeview(self, columns=result_columns, show='headings')

        self.scan_results.heading('ip', text='IP Address')
        self.scan_results.column('ip', minwidth=0, width=100)
        self.scan_results.heading('port_num', text='Port')
        self.scan_results.column('port_num', minwidth=0, width=50)
        self.scan_results.heading('port_status', text='Status')
        self.scan_results.column('port_status', minwidth=0, width=80)
        self.scan_results.heading('port_name', text='Port Name')
        self.scan_results.column('port_name', minwidth=0, width=120)
        self.scan_results.heading('description', text='Description')
        self.scan_results.column('description', minwidth=0, width=300)

        data = []
        data.append(('192.168.0.1', '135', 'Open', 'epmap', 'dce endpoint resolution, location service, etc.'))
        data.append(('192.168.0.1', '137', 'Closed', 'netbios-ns', 'netbios name service'))
        data.append(('192.168.0.1', '138', 'Closed', 'netbios-dgm', 'netbios datagram service'))
        data.append(('192.168.0.1', '139', 'Open', 'netbios-ssn', 'netbios session service'))
        data.append(('192.168.0.1', '443', 'Closed', 'https', 'secure http (ssl), http protocol over tls/ssl'))
        data.append(('192.168.0.1', '445', 'Open', 'microsoft-ds', 'microsoft-ds'))

        for x in data:
            self.scan_results.insert('', tk.END, values=x)

        self.scan_results.bind('<<TreeviewSelect>>', self.item_selected)

        self.scan_results.grid(row=1, column=0, sticky='nsew')

        # add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.scan_results.yview)
        self.scan_results.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

    def item_selected(self, event):
        for selected_item in self.scan_results.selection():
            item = self.scan_results.item(selected_item)
            record = item['values']
            # show a message
            showinfo(title='Information', message=''.join(str(record)))


# Page 2
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        """ ========================
             INITIALIZE VARIABLE(S)
            ======================== """
        # ...

        """ ====================
             PAGE CONFIGURATION
            ==================== """
        # ...


# Main Controller class - primary window container - contains, controls & views Page(s)
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        """ ========================
             INITIALIZE VARIABLE(S)
            ======================== """
        machine_ip = socket.gethostbyname(socket.gethostname())
        print(machine_ip)

        self.target = machine_ip
        self.queue = Queue()

        self.open_ports = []

        self.port_list = range(1, 1024)

        self.thread_list = []

        # Menu Bar  (configured in 'app.py')
        # NOTE: This is just the initialization of the Menu - it is ADDED to the container in 'app.py'
        self.menubar = tk.Menu(self)

        # FILE
        self.file_menu = tk.Menu(self.menubar, tearoff=0)

        self.file_menu.add_command(label='Scan')
        self.file_menu.add_command(label='Open')
        self.file_menu.add_command(label='Save')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.master.destroy)

        # VIEW
        self.view_menu = tk.Menu(self.menubar, tearoff=0)

        # SETTINGS
        self.settings_menu = tk.Menu(self.menubar, tearoff=0)

        # Settings -> Preferences
        self.preferences_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.preferences_menu.add_command(label='Keyboard Shortcuts')
        # Settings -> Preferences -> Font Preferences
        font_preferences = tk.Menu(self.preferences_menu, tearoff=0)
        font_preferences.add_command(label='Font Size')
        font_preferences.add_command(label='Font Style')

        self.preferences_menu.add_cascade(label="Font Preferences", menu=font_preferences)
        self.settings_menu.add_cascade(label="Preferences", menu=self.preferences_menu)

        # HELP
        self.help_menu = tk.Menu(self.menubar, tearoff=0)

        self.help_menu.add_command(label='Welcome')
        self.help_menu.add_command(label='About')

        # ADD ALL DROPDOWN BUTTONS TO THE MENUBAR
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        self.menubar.add_cascade(label="Settings", menu=self.settings_menu)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        """ ======================
             WINDOW CONFIGURATION
            ====================== """
        # Create object for each Page
        self.p1 = Page1(self)
        self.p2 = Page2(self)

        # Create container to hold all content  -  CONTAINS Page(s)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Place all pages (stacked atop one another) in the 'container' Frame
        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # BUTTON CONFIGURATION
        self.p1.scan_button.config(command=self.scan)

        # Display the 1st page!
        self.p1.show()

    def scan(self):
        self.fill_queue(self.port_list)

        for t in range(500):
            thread = threading.Thread(target=self.worker)
            self.thread_list.append(thread)

        for thread in self.thread_list:
            thread.start()

        for thread in self.thread_list:
            thread.join()

        print("\nOpen ports are:\n", self.open_ports)

    def PortScanner(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.target, port))

            return True
        except:
            return False

    def fill_queue(self, port_list):
        for port in port_list:
            self.queue.put(port)

    def worker(self):
        while not self.queue.empty():
            port = self.queue.get()
            if self.PortScanner(port):
                print("\nScanning...")
                print("Port {} is open!".format(port))

                self.open_ports.append(port)
