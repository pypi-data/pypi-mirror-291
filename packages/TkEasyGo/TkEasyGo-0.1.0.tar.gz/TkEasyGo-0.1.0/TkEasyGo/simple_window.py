import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb



class SimpleWindow:
    """A simple GUI window using Tkinter and ttkbootstrap with various helper methods."""
    def __init__(self, title="TkEasyGo Window", width=300, height=200):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.style = tb.Style()  # Use ttkbootstrap's style
        self.configure_styles()
        self.widgets = {}
        self.current_row = 0
        self.current_column = 0
        self.frames = {}
        self.maximized = False
        self.grid_config = {'padx': 10, 'pady': 10, 'sticky': "ew"}  # Default grid configuration

    def configure_styles(self):
        """Configure the styles for various ttkbootstrap widgets."""
        self.style.configure('TButton', padding=6, relief="flat", background="#4CAF50", font=("Arial", 12))
        self.style.configure('TLabel', background="#f4f4f4", font=("Arial", 12))
        self.style.configure('TEntry', padding=4, font=("Arial", 12))
        self.style.configure('TCheckbutton', font=("Arial", 12))
        self.style.configure('TRadiobutton', font=("Arial", 12))
        self.style.configure('TCombobox', font=("Arial", 12))
        self.style.configure('TProgressbar', thickness=20)
        self.style.configure('TNotebook', background="#f4f4f4")
        self.style.configure('TNotebook.Tab', background="#d9d9d9", padding=5)

    def update_style(self, style_name, options):
        """Update the style configuration for a given widget style."""
        self.style.configure(style_name, **options)

    def set_grid_config(self, **options):
        """Set the default grid configuration for all widgets."""
        self.grid_config.update(options)

    def _add_widget(self, widget, row=None, column=None, rowspan=1, columnspan=1):
        """Helper method to add a widget to the grid with the current configuration."""
        widget.grid(row=row if row is not None else self.current_row,
                    column=column if column is not None else self.current_column,
                    rowspan=rowspan, columnspan=columnspan, **self.grid_config)
        self.current_column += columnspan
        return widget

    def add_menu(self, menu_items):
        """Add a menu to the window."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        for menu_name, commands in menu_items.items():
            menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label=menu_name, menu=menu)
            for item_name, command in commands.items():
                menu.add_command(label=item_name, command=command)

    def add_button(self, text, command, row=None, column=None, rowspan=1, columnspan=1, style=None, frame=None):
        """Add a button to the window."""
        frame = frame or self.root
        button = ttk.Button(frame, text=text, command=command, style='TButton')
        if style:
            button.config(**style)
        self.widgets['button'] = self._add_widget(button, row, column, rowspan, columnspan)
        return button

    def add_label(self, text, row=None, column=None, rowspan=1, columnspan=1, style=None, frame=None):
        """Add a label to the window."""
        frame = frame or self.root
        label = ttk.Label(frame, text=text, style='TLabel')
        if style:
            label.config(**style)
        self.widgets['label'] = self._add_widget(label, row, column, rowspan, columnspan)
        return label

    def add_textbox(self, default_text="", width=20, row=None, column=None, rowspan=1, columnspan=1, style=None, frame=None):
        """Add a textbox (entry) to the window."""
        frame = frame or self.root
        textbox = ttk.Entry(frame, width=width, style='TEntry')
        textbox.insert(0, default_text)
        if style:
            textbox.config(**style)
        self.widgets['textbox'] = self._add_widget(textbox, row, column, rowspan, columnspan)
        return textbox

    def add_checkbox(self, text, variable, row=None, column=None, style=None, frame=None):
        """Add a checkbox to the window."""
        frame = frame or self.root
        checkbox = ttk.Checkbutton(frame, text=text, variable=variable.var, style='TCheckbutton')
        if style:
            checkbox.config(**style)
        self.widgets['checkbox'] = self._add_widget(checkbox, row, column)
        return checkbox

    def add_radiobutton(self, text, value, variable, row=None, column=None, style=None, frame=None):
        """Add a radiobutton to the window."""
        frame = frame or self.root
        radiobutton = ttk.Radiobutton(frame, text=text, value=value, variable=variable.var, style='TRadiobutton')
        if style:
            radiobutton.config(**style)
        self.widgets['radiobutton'] = self._add_widget(radiobutton, row, column)
        return radiobutton

    def add_combobox(self, values, row=None, column=None, style=None, frame=None):
        """Add a combobox to the window."""
        frame = frame or self.root
        combobox = ttk.Combobox(frame, values=values, style='TCombobox')
        if style:
            combobox.config(**style)
        self.widgets['combobox'] = self._add_widget(combobox, row, column)
        return combobox

    def add_progressbar(self, maximum=100, value=0, row=None, column=None, columnspan=1, style=None, frame=None):
        """Add a progress bar to the window."""
        frame = frame or self.root
        progressbar = ttk.Progressbar(frame, maximum=maximum, value=value, style='TProgressbar')
        if style:
            progressbar.config(**style)
        self.widgets['progressbar'] = self._add_widget(progressbar, row, column, columnspan=columnspan)
        return progressbar

    def add_slider(self, from_=0, to=100, orient=tk.HORIZONTAL, value=0, row=None, column=None, columnspan=1, style=None, frame=None):
        """Add a slider to the window."""
        frame = frame or self.root
        slider = tk.Scale(frame, from_=from_, to=to, orient=orient, length=200, sliderlength=30)
        slider.set(value)
        if style:
            slider.config(**style)
        self.widgets['slider'] = self._add_widget(slider, row, column, columnspan=columnspan)
        return slider

    def add_notebook(self, tabs, row=None, column=None, rowspan=1, columnspan=1, style=None):
        """Add a notebook (tabbed interface) to the window."""
        notebook = ttk.Notebook(self.root, style='TNotebook')
        if style:
            notebook.config(**style)
        for tab_name, content in tabs.items():
            frame = tk.Frame(notebook)
            content(self, frame)  # Pass SimpleWindow instance for content creation
            notebook.add(frame, text=tab_name)
        self.widgets['notebook'] = self._add_widget(notebook, row, column, rowspan, columnspan)
        return notebook

    def add_label_frame(self, text, row=None, column=None, rowspan=1, columnspan=1, style=None):
        """Add a labeled frame to the window."""
        frame = ttk.LabelFrame(self.root, text=text, style='TLabelFrame')
        if style:
            frame.config(**style)
        self.widgets['label_frame'] = self._add_widget(frame, row, column, rowspan, columnspan)
        return frame

    def add_spinbox(self, from_, to, increment=1, row=None, column=None, style=None, frame=None):
        """Add a spinbox to the window."""
        frame = frame or self.root
        spinbox = ttk.Spinbox(frame, from_=from_, to=to, increment=increment, style='TSpinbox')
        if style:
            spinbox.config(**style)
        self.widgets['spinbox'] = self._add_widget(spinbox, row, column)
        return spinbox

    def add_canvas(self, width, height, row=None, column=None, columnspan=1):
        """Add a canvas to the window."""
        canvas = tk.Canvas(self.root, width=width, height=height)
        self.widgets['canvas'] = self._add_widget(canvas, row, column, columnspan=columnspan)
        return canvas

    def add_text(self, text, row=None, column=None, columnspan=1, style=None):
        """Add a text label to the window."""
        text_widget = tk.Label(self.root, text=text)
        if style:
            text_widget.config(**style)
        self.widgets['text'] = self._add_widget(text_widget, row, column, columnspan=columnspan)
        return text_widget

    def bind_event(self, widget_name, event_name, handler):
        """Bind a single event to a widget."""
        widget = self.widgets.get(widget_name)
        if widget:
            widget.bind(event_name, handler)

    def bind_events(self, widget_name, events):
        """Bind multiple events to a widget."""
        widget = self.widgets.get(widget_name)
        if widget:
            for event_name, handler in events.items():
                widget.bind(event_name, handler)

    def disable_widget(self, widget_name):
        """Disable a widget."""
        widget = self.widgets.get(widget_name)
        if widget:
            widget.state(["disabled"])

    def enable_widget(self, widget_name):
        """Enable a widget."""
        widget = self.widgets.get(widget_name)
        if widget:
            widget.state(["!disabled"])

    def remove_widget(self, widget_name):
        """Remove a widget from the window."""
        widget = self.widgets.pop(widget_name, None)
        if widget:
            widget.grid_forget()
            widget.destroy()

    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()

    def maximize(self):
        """Maximize the window."""
        self.root.attributes("-fullscreen", True)
        self.maximized = True

    def minimize(self):
        """Minimize the window."""
        self.root.iconify()

    def restore(self):
        """Restore the window to its normal size."""
        self.root.attributes("-fullscreen", False)
        self.maximized = False

    def log(self, message):
        """Log a message (simple print for now, could be expanded)."""
        print(f"[LOG]: {message}")

