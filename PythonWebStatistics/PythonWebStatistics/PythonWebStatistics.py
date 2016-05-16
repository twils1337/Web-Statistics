from WebManager import WebManager

def mean(data):
    sum_total = sum(data)
    return double(sum_total) / double(length(data)) 

def median(data):
    return data[length(data)/2] if length(data)%2 != 0 else double( data[length(data)/2] + data[(length(data)/2)+1] )/2.0

def main():
    web_manager2014 = WebManager("2014")
    web_manager2015 = WebManager("2015")
    web_manager2016 = WebManager("2016")
    web_manager2014.read()
    web_manager2015.read()
    web_manager2016.read()
    web_manager2014.display_info()
    print "\n"
    web_manager2015.display_info()
    print "\n"
    web_manager2016.display_info()


if __name__ == "__main__":
    main()