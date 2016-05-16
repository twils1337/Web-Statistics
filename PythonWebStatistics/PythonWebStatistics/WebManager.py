import urllib2

class WebManager(object):
    """class that will send requests to a web site for data and fill an sqlite3 database with that data"""
    def __init__(self):
        self.year = ""
        self.url = ""
        self.wind_speed = []
        self.air_temperature = []
        self.barometric_pressure = []

    def __init__(self, year):
        self.year = str(year)
        self.url = "https://lpo.dt.navy.mil/data/DM/Environmental_Data_Deep_Moor_"+str(year)+".txt"
        self.wind_speed = []
        self.air_temperature = []
        self.barometric_pressure = []

    def read(self):
        ready_url = urllib2.urlopen(self.url)
        if ready_url.getcode() == 200:
            self.parse(ready_url)
            sorted(self.wind_speed)
            sorted(self.air_temperature)
            sorted(self.barometric_pressure)
        else:
            print ("Error: Site not available.")
        ready_url.close()
        
    def parse(self, site):
        site.readline()    #headers for each column
        init_read = site.readlines()
        for lines in init_read:
            columns = lines.split()
            self.wind_speed.append(float(columns[8]))
            self.air_temperature.append(float(columns[2]))
            self.barometric_pressure.append(float(columns[3]))

    def display_mean(self):
        sum_wind_speed = sum(self.wind_speed)
        sum_air_temp = sum(self.air_temperature)
        sum_b_press = sum(self.barometric_pressure)
        item_count = len(self.wind_speed)
        print "\tMean:"
        mean_ws = float(sum_wind_speed)/float(item_count)
        mean_at = float(sum_air_temp)/float(item_count)
        mean_bp = float(sum_b_press)/float(item_count)
        print ("\t\tWind Speed: %.2f" % mean_ws)
        print ("\t\tAir Temperature: %.2f" % mean_at)
        print ("\t\tBarometric Pressure: %.2f" % mean_bp)

    def display_median(self):
        size = len(self.wind_speed)
        print "\tMedian:"
        med_ws = self.wind_speed[size/2] if size%2 == 1 else float(self.wind_speed[size/2] + self.wind_speed[(size/2)+1])/2.0
        med_at = self.air_temperature[size/2] if size%2 == 1 else float(self.air_temperature[size/2] + self.air_temperature[(size/2)+1])/2.0
        med_bp = self.barometric_pressure[size/2] if size%2 == 1 else float(self.barometric_pressure[size/2] + self.barometric_pressure[(size/2)+1])/2.0
        print ("\t\tWind Speed: %.2f" % med_ws)
        print ("\t\tAir Temperature: %.2f" % med_at)
        print ("\t\tBarometric Pressure: %.2f" % med_bp)

    def display_info(self):
        print "Year: " + self.year
        self.display_mean()
        self.display_median()