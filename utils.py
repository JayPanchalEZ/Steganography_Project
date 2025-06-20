from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def browse_image():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.update()
    filename = askopenfilename(
        title="Select Image",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    root.destroy()
    return filename

def choose_save_path(default_name="output.png"):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    root.update()
    filepath = asksaveasfilename(
        title="Save Image As",
        defaultextension=".png",
        initialfile=default_name,
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    root.destroy()
    return filepath