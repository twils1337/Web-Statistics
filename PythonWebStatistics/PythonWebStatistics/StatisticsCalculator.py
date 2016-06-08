import sqlite3

yrs = ('2014','2015', '2016')
attribs = ('Wind_speed','Air_temp','Barometric_press')

class StatisticsCalculator(object):
    """Handles all the calculation for the data from the lake pend oreille web site."""
    def __init__(self, db):
        self.wind_speed = dict((yr,[]) for yr in yrs)
        self.air_temperature = dict((yr,[]) for yr in yrs)
        self.barometric_pressure = dict((yr,[]) for yr in yrs)
        self.averages = {yr:{attrib:0.0}
                            for yr in yrs
                            for attrib in attribs}
        self.medians = {yr:{attrib:0.0}
                            for yr in yrs
                            for attrib in attribs}
        self.db = db

    def parse_n_calc_data(self,year):
       self.parse_data(year)
       self.calc_avgs(year)
       self.calc_meds(year)

    def parse_data(self, year):
        try:
            db_connect = sqlite3.connect(self.db)
        except sqlite3.Error as e:
            print ('Error: {}'.format(e.message))
        db_connect.row_factory = sqlite3.Row
        cursor = db_connect.cursor()
        command = '''SELECT  Wind_speed, Air_temp, Barometric_press\
                     FROM raw_data\
                     WHERE strftime('%Y',Date) = \'{}\''''.format(year)
        cursor.execute(command)
        for row in cursor:
            self.wind_speed[year].append(row['Wind_speed'])
            self.air_temperature[year].append(row['Air_temp'])
            self.barometric_pressure[year].append(row['Barometric_press'])
        self.wind_speed[year].sort()
        self.air_temperature[year].sort()
        self.barometric_pressure[year].sort()
        db_connect.close()

    def get_container_str(self, container):
        container_str = "None"
        if id(container) == id(self.wind_speed):
            container_str = "Wind_speed"
        elif id(container) == id(self.air_temperature):
            container_str = "Air_temp"
        elif id(container) == id(self.barometric_pressure):
            container_str = "Barometric_press"
        return container_str

    def indexForYear(self, year):
        yr = -1
        if year == '2014':
            yr = 0
        elif year == '2015':
            yr = 1
        else: # year == '2016'
            yr = 2
        return yr  

    def indexForContainer(self, container_str):
        if container_str =="Wind_speed":
            return 0
        elif container_str == "Air_temp":
            return 1
        elif container_str == "Barometric_press":
            return 2
        else:
            return -1

    def calc_avgs(self, year):
        try:
            db_connect = sqlite3.connect(self.db)
        except sqlite3.Error as e:
            print ('Error: {}'.format(e.message))
        cursor = db_connect.cursor()
        for attrib in attribs:
            command = '''SELECT avg({0})\
                            FROM raw_data\
                            WHERE strftime('%Y',Date) = \'{1}\''''.format(attrib, year)
            cursor.execute(command)
            yr_avg = cursor.fetchone()
            self.averages[year][attrib] = yr_avg[0]
        db_connect.close()

    def calc_meds(self, year):
        self.medians[year]['Wind_speed'] = self.getMed(self.wind_speed, year)
        self.medians[year]['Air_temp'] = self.getMed(self.air_temperature, year)
        self.medians[year]['Barometric_press'] = self.getMed(self.barometric_pressure, year)

    def getMed(self, container, yr):
        size = len(self.wind_speed[yr])
        mid = size//2
        med = container[yr][mid] if mid%2 == 1\
               else (container[yr][mid]+container[yr][mid+1])/2.0
        return med

    def display_info(self, year):
        print("Year: " + year)
        self.display_mean(year)
        print
        self.display_median(year)

    def display_mean(self, year):
        print ('''\
        Mean:
        \tWind Speed: {:.2f}
        \tAir Temperature: {:.2f}
        \tBarometric Pressure: {:.2f}'''.format(self.averages[year]['Wind_speed'],
                                                self.averages[year]['Air_temp'],
                                                self.averages[year]['Barometric_press']))

    def display_median(self, year):
        print ('''\
        Median:
        \tWind Speed: {:.2f}
        \tAir Temperature: {:.2f}
        \tBarometric Pressure: {:.2f}'''.format(self.medians[year]['Wind_speed'],
                                                self.medians[year]['Air_temp'],
                                                self.medians[year]['Barometric_press']))
        

