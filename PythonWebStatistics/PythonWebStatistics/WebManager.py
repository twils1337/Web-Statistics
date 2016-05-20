import urllib2
import sqlite3

db = "C:\\Users\\Tyler\\Desktop\\Databases\\Lake_Pend_Oreille.db"
url_prefix = "https://lpo.dt.navy.mil/data/DM/Environmental_Data_Deep_Moor_"

class WebManager(object):
    """class that will send requests to a web site for data and fill an sqlite3 database with that data"""
    def __init__(self):
        self.url = ''
        self.wind_speed = [[] for i in range(3)]
        self.air_temperature = [[] for i in range(3)]
        self.barometric_pressure = [[] for i in range(3)]
        self.averages = [[0.0 for i in range(3)] for i in range(3)]
        self.medians = [[0.0 for i in range(3)] for i in range(3)]

    def load(self):
        try:
            db_connect = sqlite3.connect(db)
        except sqlite3.Error as e:
            print ('Error: {}'.format(e.message))
        try:
            for yr in ('2014', '2015', '2016'):
                print ('Loading raw data from {}...'.format(yr))
                if (self.isYearLoaded(db_connect, yr)):
                    print '{} data already loaded. Continuing...\n'.format(yr)
                    continue
                else:
                    tableData = self.getTable(yr)
                    db_connect.executemany('INSERT INTO raw_data(ID, Date, Time, Air_temp, Barometric_press, Dew_point,\
                                                                 Relative_humidity, Wind_dir, Wind_gust, Wind_speed\
                                                                )\
                                                        VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tableData)
                    print ('Successfully fetched {} data.\n'.format(yr))
        except sqlite3.Error as e:
            print ('Error: {}'.format(e.message))
            db_connect.close()
            return
        db_connect.commit()
        db_connect.close()

    def isYearLoaded(self, db_connect, year):
        tableSizeQuery = '''SELECT COUNT(*)\
                            FROM raw_data\
                            WHERE strftime('%Y',Date) = \'{}\''''.format(year)
        cursor = db_connect.cursor()
        cursor.execute(tableSizeQuery)
        queryRet = cursor.fetchone()
        ret = int(queryRet[0])
        return True if int(queryRet[0]) > 0 else False

    def getTable(self, year):
        try:
            url_connect = urllib2.urlopen(url_prefix+'{}.txt'.format(year))
        except urllib2.HTTPError as e:
            print ('Error code {0}: {1}'.format(e.code, e.reason))
        url_connect.readline()
        read = url_connect.read().splitlines()
        table = [line.split() for line in read]
        table = self.structureDate(table)
        url_connect.close()
        return table

    def structureDate(self, table):
            # 0 element is date component
            for row in table:
                row[0] = row[0].replace('_','-')
            return table

    def parse_n_calc_data(self,year):
       self.container_query(self.wind_speed, year)
       self.container_query(self.air_temperature, year)
       self.container_query(self.barometric_pressure, year)
       self.calc_avgs(year)
       self.calc_meds(year)

    def container_query(self, container, year):
        try:
            db_connect = sqlite3.connect(db)
        except sqlite3.Error as e:
            print ('Error: {}'.format(e.message))
        cursor = db_connect.cursor()
        container_str = self.get_container_str(container)
        command = '''SELECT  {0}\
                     FROM raw_data\
                     WHERE strftime('%Y',Date) = \'{1}\'\
                     ORDER BY {0} DESC'''.format(container_str, year)
        cursor.execute(command)
        yr_i = self.indexForYear(year)
        container[yr_i][:] = sorted([float(i[0]) for i in cursor.fetchall()])
        db_connect.close()
        
    def display_info(self, year):
        print "Year: " + year
        self.display_mean(year)
        print
        self.display_median(year)

    def display_mean(self, year):
        yr_i = self.indexForYear(year)
        print '''\
        Mean:
        \tWind Speed: {:.2f}
        \tAir Temperature: {:.2f}
        \tBarometric Pressure: {:.2f}'''.format(self.averages[yr_i][0],self.averages[yr_i][1],self.averages[yr_i][2])

    def display_median(self, year):
        yr_i = self.indexForYear(year)
        print '''\
        Median:
        \tWind Speed: {:.2f}
        \tAir Temperature: {:.2f}
        \tBarometric Pressure: {:.2f}'''.format(float(self.medians[yr_i][0]), float(self.medians[yr_i][1]), float(self.medians[yr_i][2]))

    def get_container_str(self, container):
        container_str = "None"
        if id(container) == id(self.wind_speed):
            container_str = "Wind_speed"
        elif id(container) == id(self.air_temperature):
            container_str = "Air_temp"
        elif id(container) == id(self.barometric_pressure):
            container_str = "Barometric_press"
        return container_str

    def calc_avgs(self, year):
        try:
            db_connect = sqlite3.connect(db)
        except sqlite3.Error as e:
            print ('Error: {}'.format(e.message))
        cursor = db_connect.cursor()
        container_str = "None"
        yr_avg = list()
        yr_i = self.indexForYear(year)
        cont_i = -1
        for i, avg in enumerate(self.averages[yr_i]):
            if i == 0:
                container_str = self.get_container_str(self.wind_speed)
            elif i == 1:
                container_str = self.get_container_str(self.air_temperature)
            else:
                container_str = self.get_container_str(self.barometric_pressure)
            cont_i = self.indexForContainer(container_str)
            command = '''SELECT avg({0})\
                            FROM raw_data\
                            WHERE strftime('%Y',Date) = \'{1}\''''.format(container_str, year)
            cursor.execute(command)
            yr_avg.append(float(cursor.fetchone()[0]))
            self.averages[yr_i] = yr_avg
        db_connect.close()

    def calc_meds(self, year):
        yr_i = self.indexForYear(year)
        size = len(self.wind_speed[yr_i])
        mid = size//2
        ws_med = self.getMed(self.wind_speed, yr_i, mid)
        at_med = self.getMed(self.air_temperature, yr_i, mid)
        bp_med = self.getMed(self.barometric_pressure, yr_i, mid)
        yr_meds = [ws_med, at_med, bp_med]
        self.medians[yr_i] = yr_meds
        
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

    def getMed(self, container, yr_i, mid):
        med = container[yr_i][mid] if mid%2 == 1\
               else (container[yr_i][mid]+container[yr_i][mid+1])/2.0
        return med
