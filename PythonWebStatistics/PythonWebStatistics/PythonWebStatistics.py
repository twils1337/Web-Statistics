from WebManager import WebManager
import os
import time


def main():
    wm = WebManager()
    wm.load()
    time.sleep(4)
    os.system('cls')
    for yr in ('2014', '2015', '2016'):
        wm.parse_n_calc_data(yr)
        wm.display_info(yr)
        print "\n"
if __name__ == "__main__":
    main()
