import urllib.request
import requests

class Stock():
    # Constant(s)
    BASE_URL = "http://ichart.finance.yahoo.com/table.csv?s="
    # individual breaks the file into it's own list
    # individual_list[0] will give you the first row
    # individual_list[0][0] will give you the first row first column attribute
    INDIVIDUAL_LIST = []

    def __int__(self):
        pass

    def validate_file(self, ticker_symbol):
        while True:
            open_url = self.BASE_URL + ticker_symbol
            try:
                urllib.request.urlopen(open_url)
            except urllib.error.URLError as e:
                print("Oops! {}. Incorrect ticker symbol. Try again...".format(e))
                break
            else:
                response_file = urllib.request.urlopen(self.BASE_URL + ticker_symbol)
                processed_file = self.process_file(response_file)
                print(processed_file)
                # print("Opening Average:", self.average_open(processed_file))
            finally:
                break

    def user_input(self, ticker_symbol):
        while True:
            if ticker_symbol.isspace():
                print("Oops! Empty input. Try again...")
                break
            else:
                self.validate_file(ticker_symbol)
                break

    def process_file(self, opened_response_file):
        for row in opened_response_file:
            row = row.decode('utf-8')
            row_split = row.split(',')
            self.INDIVIDUAL_LIST.append(row_split)
        self.INDIVIDUAL_LIST.pop(0)
        for item in self.INDIVIDUAL_LIST:
            item.pop(0)
        return self.INDIVIDUAL_LIST

    #response_file is after the file has been processed through process_file.
    def average_open(self):
        total_sum = 0
        counter = 0
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        print("LIST:", NEW_FLOAT_LIST)
        for items in NEW_FLOAT_LIST:
            open_list.append(items[0])
        for items in open_list:
            total_sum += items
            counter += 1
        average = total_sum / counter
        return average

    def average_high(self):
        total_sum = 0
        counter = 0
        open_list = []
        for items in self.INDIVIDUAL_LIST:
            open_list.append(items[1])
        open_list = open_list[1:]
        for items in open_list:
            items = float(items)
            total_sum += items
            counter += 1
        average = total_sum / counter
        return average

    def average_low(self):
        total_sum = 0
        counter = 0
        open_list = []
        for items in self.INDIVIDUAL_LIST:
            open_list.append(items[2])
        open_list = open_list[1:]
        for items in open_list:
            items = float(items)
            total_sum += items
            counter += 1
        average = total_sum / counter
        return average

    def average_close(self):
        total_sum = 0
        counter = 0
        open_list = []
        self.INDIVIDUAL_LIST = self.INDIVIDUAL_LIST[1:]
        print(self.INDIVIDUAL_LIST)
        for items in self.INDIVIDUAL_LIST:
            try:
                open_list.append(float(items[3]))
            except (ValueError, TypeError):
                return 0.0
        for items in open_list:
            total_sum += items
            counter += 1
        average = total_sum / counter
        return average

    def average_volume(self):
        total_sum = 0
        counter = 0
        open_list = []
        self.INDIVIDUAL_LIST = self.INDIVIDUAL_LIST[1:]
        for items in self.INDIVIDUAL_LIST:
            try:
                open_list.append(float(items[4]))
            except (ValueError, TypeError):
                return 0.0
        for items in open_list:
            total_sum += items
            counter += 1
        average = total_sum / counter
        return average

    # PAGE TWO METHODS
    # OPEN
    def pageTwo_Open(self, days):
        # give me the list of open
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        # 0:90 means for the first three months
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[0])
        return open_list

    def pageTwo_lengthOpen(self,days):
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        # 0:90 means for the first three months
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[0])
        return len(open_list)

    # HIGH
    def pageTwo_High(self, days):
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        # 0:90 means for the first three months
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[1])
        return open_list

    def pageTwo_lengthHigh(self, days):
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[1])
        return len(open_list)

    # LOW
    def pageTwo_Low(self, days):
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[2])
        return open_list

    def pageTwo_lengthLow(self, days):
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[2])
        return len(open_list)

    # Close
    def pageTwo_Close(self, days):
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[3])
        return open_list

    def pageTwo_lengthClose(self, days):
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[3])
        return len(open_list)

    # Volume
    def pageTwo_Volume(self, days):
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[3])
        return open_list

    def pageTwo_lengthVolume(self, days):
        open_list = []
        NEW_FLOAT_LIST = [[float(j) for j in i] for i in self.INDIVIDUAL_LIST]
        NEW_FLOAT_LIST = NEW_FLOAT_LIST[0:days]
        for items in NEW_FLOAT_LIST:
            open_list.append(items[3])
        return len(open_list)

