import sqlite3

yrs = ('2014','2015', '2016')
attribs = ('Wind_speed','Air_temp','Barometric_press')
#number rep. of month to letter rep. of month
N2L_month = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', 
             '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

Debug = False

class StatisticsCalculator(object):
    """Handles all the calculation for the data from the lake pend oreille web site."""
    def __init__(self, db):
        self.wind_speed = []
        self.air_temperature = []
        self.barometric_pressure = []
        self.averages = {attribute:0.0 for attribute in attribs}
        self.medians =  {attribute:0.0 for attribute in attribs}
        self.db = db

    def reset(self):
        self.wind_speed = []
        self.air_temperature = []
        self.barometric_pressure = []
        self.averages = {attribute:0.0 for attribute in attribs}
        self.medians =  {attribute:0.0 for attribute in attribs}

    def parse_n_calc_data(self, year, month, day):
        self.reset()
        self.parse_data(year, month, day)
        for attribute in ['Wind_speed','Air_temp','Barometric_press']:
            self.calc_avgs(attribute, year, month, day)
            self.calc_meds(attribute, year, month, day)

    def create_date_list(self, year, month, day):
        if month == '-1': #day can't be valid if there's no month -> only year valid
            return [year]
        elif day != '-1': #month has to be valid if there is a day -> year,month,day valid
            return [year,month,day]
        else: #only year and month valid
            return [year,month]

    def append_date_filter(self, date):
        date_appendage = ''
        if len(date) == 3:
            if len(date[2]) == 1: date[2] = '0' + date[2]
            if len(date[1]) == 1: day = '0' + date[1]
            date_appendage = 'WHERE strftime(\'%Y-%m-%d\',Date) = \'{y}-{m}-{d}\''.format(y=date[0], m=date[1], d=date[2])
        if len(date) == 2:
            if len(date[1]) == 1: month = '0' + month
            date_appendage = 'WHERE strftime(\'%Y-%m\',Date) = \'{y}-{m}\''.format(y=date[0], m=date[1])
        else: #query whole year
            date_appendage = 'WHERE strftime(\'%Y\',Date) = \'{y}\''.format(y=date[0])
        return date_appendage

    def parse_data(self, year, month, day):
        try:
            db_connect = sqlite3.connect(self.db)
        except sqlite3.Error as e:
            print ('Error: {}'.format(e.message))
        db_connect.row_factory = sqlite3.Row
        cursor = db_connect.cursor()
        command = '''SELECT  Wind_speed, Air_temp, Barometric_press\
                     FROM raw_data '''
        command += self.append_date_filter( self.create_date_list(year,month,day) )
        cursor.execute(command)
        for row in cursor:
            self.wind_speed.append(row['Wind_speed'])
            self.air_temperature.append(row['Air_temp'])
            self.barometric_pressure.append(row['Barometric_press'])
        self.wind_speed.sort()
        self.air_temperature.sort()
        self.barometric_pressure.sort()
        db_connect.close()

    def calc_avgs(self, attribute, year, month, day):
        try:
            db_connect = sqlite3.connect(self.db)
        except sqlite3.Error as e:
            print ('Error: {}'.format(e.message))
        cursor = db_connect.cursor()
        command = '''SELECT avg({a})\
                     FROM raw_data '''.format(a=attribute)
        command += self.append_date_filter( self.create_date_list(year,month,day) )
        cursor.execute(command)
        yr_avg = cursor.fetchone()
        self.averages[attribute] = yr_avg[0]
        db_connect.close()

    def calc_meds(self, attribute, year, day, month):
        self.medians['Wind_speed'] = self.getMed(self.wind_speed)
        self.medians['Air_temp'] = self.getMed(self.air_temperature)
        self.medians['Barometric_press'] = self.getMed(self.barometric_pressure)

    def getMed(self, attribute_container):
        size = len(self.wind_speed)
        mid = size//2
        med = attribute_container[mid] if size & 1 else (attribute_container[mid]+attribute_container[mid-1])/2.0
        return med

    def get_date_str(self, year, month, day):
        date_fields_valid = len( self.create_date_list(year,month,day) )
        date_str = ''
        if date_fields_valid == 3:
            date_str = '{m} {d}, {y}'.format(m=N2L_month[month], d=day if day[0] != '0' else day[1], y=year)
        elif date_fields_valid == 2:
            date_str = '{m}, {y}'.format(m=N2L_month[month], y=year)
        else:
            date_str = year
        return date_str

    def display_info(self, year, month, day):
        date_str = self.get_date_str(year, month, day)
        disp_str = '''Date: {d}\t{mean}\n{med}'''.format(d=date_str, mean=self.mean_format(), med=self.med_format())
        if Debug: print(disp_str)
        return disp_str

    def mean_format(self):
        str_form = '''
        Mean:
        \tWind Speed: {:.2f}
        \tAir Temperature: {:.2f}
        \tBarometric Pressure: {:.2f}\n'''.format(self.averages['Wind_speed'],
                                                self.averages['Air_temp'],
                                                self.averages['Barometric_press'])
        return str_form

    def med_format(self):
        str_form = '''\
        Median:
        \tWind Speed: {:.2f}
        \tAir Temperature: {:.2f}
        \tBarometric Pressure: {:.2f}'''.format(self.medians['Wind_speed'],
                                                self.medians['Air_temp'],
                                                self.medians['Barometric_press'])
        return str_form

    def get_query_data(self, year, month, day):
        self.parse_n_calc_data(year,month,day)
        return self.display_info(year,month,day)
        

