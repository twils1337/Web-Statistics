import tkinter as tk
from StatsApp import StatsApp
import os
import time
import sys


def main():

    root = tk.Tk()
    Stats_app = StatsApp(root, db = sys.argv[1])
    root.mainloop()

if __name__ == '__main__':
    main()
