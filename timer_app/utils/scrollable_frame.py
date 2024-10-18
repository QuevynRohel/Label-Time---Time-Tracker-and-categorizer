import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Canvas for the scrollable content
        self.canvas = tk.Canvas(self) #, bg="#aa00dd"
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame for the content inside the canvas
        self.scrollable_frame = tk.Frame(self.canvas) # bg="#0000dd"

        # When the scrollable_frame changes, resize the canvas accordingly
        self.scrollable_frame.bind("<Configure>", self.on_configure)

        # Create a window in the canvas, initially anchored to the north
        self.window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Scroll with the mouse wheel
        self.scrollable_frame.bind_all("<MouseWheel>", self._on_mousewheel)
        parent.after(100, lambda: self.on_configure(None))

    def on_configure(self, event):
        # Configure the scroll region for the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Get the width of the canvas and scrollable frame
        canvas_width = self.canvas.winfo_width()
        frame_width = self.scrollable_frame.winfo_reqwidth()
        # Center the frame horizontally inside the canvas
        if frame_width < canvas_width:
            self.canvas.itemconfig(self.window, width=canvas_width)
        else:
            self.canvas.itemconfig(self.window, width=frame_width)
        self.canvas.update_idletasks()

    def _on_mousewheel(self, event):
        # Scroll vertically with the mouse wheel
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")
    
    def get_frame(self):
        return self.scrollable_frame
