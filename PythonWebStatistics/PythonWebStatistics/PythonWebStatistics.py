from WebManager import WebManager
from StatisticsCalculator import StatisticsCalculator
import tkinter as tk
import StatsApp as app
import os
import time
import sys


def main():
    '''
    wm = WebManager(db = sys.argv[1])
    wm.load()
    stat_calc = StatisticsCalculator(db = sys.argv[1]);
    input('Hit enter to continue.')
    os.system('cls')
    for yr in ('2014', '2015', '2016'):
        stat_calc.parse_n_calc_data(yr)
        stat_calc.display_info(yr)
        print ('\n')
    '''
    root = tk.Tk()
    app.StatsApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
