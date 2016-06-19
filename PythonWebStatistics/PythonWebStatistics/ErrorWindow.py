import tkinter as tk
class ErrorWindow(object):
    """Class that displays errors as a pop up self.err_top_lvl."""
    def __init__(self, msg):
        self.err_top_lvl = tk.Toplevel()
        err_label = tk.Label(self.err_top_lvl, text = msg)
        err_label.pack()
        self.center()

    def center(self): 
        scrn_width = self.err_top_lvl.winfo_screenwidth()
        scrn_height = self.err_top_lvl.winfo_screenheight()
        win_width, win_height = tuple(int(_) for _ in self.err_top_lvl.geometry().split('+')[0].split('x'))
        pos_x = scrn_width//2 - win_width//2
        pos_y = scrn_height//2 - win_height//2
        self.err_top_lvl.geometry('{}x{}+{}+{}'.format(win_width, win_height,pos_x,pos_y))
    
