__all__ = ['Page', 'Page1', 'Page2', 'MainView']

# NOTE:  Add an exception for checking VALID IP INPUT  (before actually running the IP)

# Import Libs
import os
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.messagebox import showinfo

import socket
import queue
import threading
from concurrent.futures import ThreadPoolExecutor


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
        self.data = []  # For storing scanned port data

        """ ====================
             PAGE CONFIGURATION
            ==================== """
        # Scan button
        self.scan_button = tk.Button(self, text="Scan", font=self.medium_font)
        self.scan_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # IP Address label
        self.ip_label = tk.Label(self, text="IP Address:", font=self.small_font)
        self.ip_label.grid(row=0, column=1, padx=0, pady=5, sticky="w")
        # IP Address text input
        self.ip_entry_text = tk.StringVar()
        self.ip_entry_text.set("localhost")
        self.ip_entry = tk.Entry(self, textvariable=self.ip_entry_text, font=self.small_font)
        self.ip_entry.grid(row=0, column=2, padx=0, pady=5, sticky="w")
        # 'This Machine?' Checkbox
        self.ip_default_checkbox_var = tk.IntVar()
        self.ip_default_checkbox = tk.Checkbutton(self, text="This Machine?", variable=self.ip_default_checkbox_var,
                                                  onvalue=1, offvalue=0, height=2, width=10,
                                                  command=self.toggle_default_ip)
        self.ip_default_checkbox.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Result table
        result_columns = ('ip', 'port_num', 'port_status', 'port_name', 'description')
        self.scan_results = ttk.Treeview(self, columns=result_columns, show='headings')

        # Set table heading names & column sizing
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

        # Set the action binding for when a table entry is clicked/selected
        self.scan_results.bind("<<TreeviewSelect>>", self.item_selected)

        # Place/position the results table
        self.scan_results.grid(row=1, column=0, padx=(5, 0), pady=5, columnspan=60, sticky="nsew")

        # add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.scan_results.yview)
        self.scan_results.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=60, sticky="ns")

        # REMOVE FOCUS FROM WIDGET BY CLICKING OFF
        self.bind_all("<1>", lambda event: event.widget.focus_set())

    # Method for deleting port 'data' variable
    def delete_data(self):
        self.data = []

    # Method for adding a port entry to the 'data' variable
    def add_data(self, ip, port, is_open, name, description):
        self.data.append((ip, port, is_open, name, description))

    # Method to clear the results table
    def clear_table(self):
        for item in self.scan_results.get_children():
            self.scan_results.delete(item)

    # Method to update the table with the stored data ('data' var)
    def update_table(self):
        # Clear all current table data
        self.clear_table()
        # Add all new data
        for item in self.data:
            temp = [item[0],
                    item[1],
                    # Set status to 'Open'/'Closed' if is_open == True/False
                    'Open' if item[2] else 'Closed',
                    item[3],
                    item[4]]
            self.scan_results.insert('', tk.END, values=temp)

    def toggle_default_ip(self):
        if self.ip_default_checkbox_var.get() == 1:
            self.ip_entry.config(state='disabled')
            self.ip_entry_text.set("localhost")
        elif self.ip_default_checkbox_var.get() == 0:
            self.ip_entry.config(state='normal')

    def item_selected(self, event):
        for selected_item in self.scan_results.selection():
            item = self.scan_results.item(selected_item)
            record = item['values']
            # show a message
            showinfo(title='Information', message=''.join(str(record)))


# Page 2  -  Welcome
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
        # Back button
        self.back_button = tk.Button(self, text="Back", font=self.small_font)

        # LabelFrame
        self.frame = tk.LabelFrame(self, text="Thank you for using PortScanner!", font=self.title_font)

        # Content labels
        self.label1 = tk.Label(self.frame, text="About Us", font=self.medium_font)
        self.label2 = tk.Label(self.frame, text="We are...", font=self.small_font)

        # Place / position everything
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.label1.grid(row=0, column=0, padx=2, pady=4)
        self.label2.grid(row=1, column=0, padx=2, pady=4)


# Main Controller class - primary window container - contains, controls & views Page(s)
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.queue = None  # Initialize queue

        """ ========================
             INITIALIZE VARIABLE(S)
            ======================== """
        self.machine_ip = socket.gethostbyname(socket.gethostname())

        # Initialize host target
        self.target = self.machine_ip

        # Initialize range of ports to scan
        self.port_list = range(1024)

        # INITIALIZE the Menubar
        # NOTE: This is ADDED TO THE CONTAINER in 'app.py'
        self.menubar = self.initialize_menubar()

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
        self.p1.scan_button.config(command=self.start_scan)
        self.p2.back_button.config(command=self.goto_main_page)

        # Display the 1st page!
        self.p1.show()

    # Method to initialize the menubar  -  returns instance of Menubar
    def initialize_menubar(self):
        menubar = tk.Menu(self)

        # FILE
        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_command(label='Scan', command=self.start_scan)
        file_menu.add_separator()
        file_menu.add_command(label='Save')
        file_menu.add_command(label='Save As...')
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.master.destroy)

        # VIEW
        view_menu = tk.Menu(menubar, tearoff=0)

        # SETTINGS
        settings_menu = tk.Menu(menubar, tearoff=0)

        #
        # Settings  ->  Preferences
        preferences_menu = tk.Menu(settings_menu, tearoff=0)
        preferences_menu.add_command(label='Keyboard Shortcuts')

        # Settings  ->  Preferences  ->  Font Preferences
        font_preferences = tk.Menu(preferences_menu, tearoff=0)
        font_preferences.add_command(label='Font Size')
        font_preferences.add_command(label='Font Style')

        # ADD SUB-MENU CASCADES TO MENU OPTIONS
        preferences_menu.add_cascade(label='Font Preferences', menu=font_preferences)
        settings_menu.add_cascade(label='Preferences', menu=preferences_menu)

        # HELP
        help_menu = tk.Menu(menubar, tearoff=0)

        help_menu.add_command(label='Welcome', command=self.goto_welcome_page)
        help_menu.add_command(label='About')

        # ADD ALL DROPDOWN BUTTONS TO THE MENUBAR
        menubar.add_cascade(label='File', menu=file_menu)
        menubar.add_cascade(label='View', menu=view_menu)
        menubar.add_cascade(label='Settings', menu=settings_menu)
        menubar.add_cascade(label='Help', menu=help_menu)

        return menubar

    # Method for lifting Page1 to the top of the stack
    def goto_main_page(self):
        self.p1.show()

    # Method for lifting Page2 to the top of the stack
    def goto_welcome_page(self):
        self.p2.show()

    # Method for starting the Port Scanning process
    def start_scan(self):
        # Update the target host with IP address FROM THE TEXTBOX
        self.target = self.p1.ip_entry_text.get()

        # Delete all data (to be replaced by updated scan data results)
        self.p1.delete_data()

        # Initialize queue
        self.queue = queue.Queue()

        # Start the PortScanner thread  (send the parameters: target ip & range of ports)
        ThreadedPortScanner(self.queue, args=(self.target, self.port_list)).start()

        # Check the progress (run self.process_queue() method) after 100ms passes
        self.master.after(100, self.process_queue)

    # Method for checking the progress of the PortScanning thread (for checking completion)
    def process_queue(self):
        try:  # If the thread process has completed (when 'data' has been added to the queue)
            msg = self.queue.get_nowait()  # Retrieving data from PortScanner thread queue
            self.p1.data = msg  # Updating the 'data' variable
            self.p1.update_table()  # Updating the result table
        except queue.Empty:  # Otherwise...
            # Re-check (run the method again) after another 100ms
            self.master.after(100, self.process_queue)


# PortScanner thread (runs separately from the main tkinter GUI thread)
class ThreadedPortScanner(threading.Thread):
    def __init__(self, q, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)

        self.queue = q  # Set the queue

        # Retrieve the given parameters (convert the Iterable to a list)
        params = []
        for x in args:
            params.append(x)

        self.target = params[0]  # Set the 1st parameter (target ip) as a variable
        self.port_list = params[1]  # Set the 2nd parameter (port range) as a variable

        # Initialize the 'data' list
        self.data = []

    # What happens during the thread process
    def run(self):
        print("\nSCANNING...")

        # Start the port scan
        self.scan()

        # (after the port scan is done)
        # Send the 'data' to the queue (which is caught in the Tkinter GUI thread, and retrieved there)
        self.queue.put(self.data)

    # Method to check if a port is open
    def is_port_open(self, target, port):
        # Define socket with exceptions
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)  # Set timeout to 3 seconds max

            try:  # Is the socket able to be connected?  (port open)
                sock.connect((target, port))
                return True  # port is open
            except:  # If an exception is caught  (port closed)
                return False  # port is not open

    def scan(self):
        # Create Thread Pool (as 'executor')
        with ThreadPoolExecutor(len(self.port_list)) as executor:
            # Call map() to run and execute the is_port_open() method over all ports in the 'port_list'
            result = executor.map(self.is_port_open, [self.target]*len(self.port_list), self.port_list)

            # Iterate the results + port numbers
            for port, is_open in zip(self.port_list, result):
                # ADD PORT ENTRY to 'data' variable
                self.data.append((
                    self.target, port, is_open, self.get_port_name(port), self.get_port_description(port)
                ))

                # If the port is open, output to console
                if is_open:
                    print(f'Port {port} is open!')

    def get_port_name(self, port):
        return f'Port {port} NAME'  # placeholder

    def get_port_description(self, port):
        return f'Port {port} DESCRIPTION'  # placeholder
