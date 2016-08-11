import urllib.request
import sqlite3
import time

url_prefix = "https://lpo.dt.navy.mil/data/DM/Environmental_Data_Deep_Moor_"

class DataManager(object):
    """class that will send requests to a web site for data and fill an sqlite3 database with that data"""
    def __init__(self, db):
        self.url = ''
        self.db = db

    def load(self):
        try:
            db_connect = sqlite3.connect(self.db)
        except sqlite3.Error as e:
            print ('Error: {}'.format(e.message))
        try:
            for yr in ('2014', '2015', '2016'):
                if not self.isYearLoaded(db_connect, yr):
                    tableData = self.getTable(yr)
                    db_connect.executemany('INSERT INTO raw_data(ID, Date, Time, Air_temp, Barometric_press, Dew_point,\
                                            Relative_humidity, Wind_dir, Wind_gust, Wind_speed\
                                            )\
                                            VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tableData)
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
            url_connect = urllib.request.urlopen(url_prefix+'{}.txt'.format(year))
        except urllib2.HTTPError as e:
            print ('Error code {0}: {1}'.format(e.code, e.reason))
        url_connect.readline()
        read = url_connect.read().splitlines()
        table = [line.split() for line in read]
        table = self.structureDate4sqlite(table)
        url_connect.close()
        return table

    def structureDate4sqlite(self, table):
            # 0 element is date component
            for row in table:
                row[0] = row[0].replace('_','-')
            return table




