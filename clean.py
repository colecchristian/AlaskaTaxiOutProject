import csv
import re

def readInCSV():
    dataSet = []
    with open('flight_data_SAN.csv', newline='\n') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|')
        count = 0

        #Read in orginal data set
        for row in data:
            obj = {}
            if count > 0:
                obj["airline"] = row[0]
                obj["flightNumber"] = row[1]
                obj["origin"] = row[2]
                obj["destination"] = row[3]
                obj["seatCount"] = row[4]
                obj["aircraft"] = row[5]
                obj["depGate"] = row[6]
                obj["arrGate"] = row[7]
                obj["schDepartTime"] = row[8]
                obj["schArriveTime"] = row[9]
                obj["actualDepartTime"] = row[10]
                obj["actualArriveTime"] = row[11]
                obj["airTime"] = row[12]
                obj["taxiOut"] = row[13]
                obj["taxiIn"] = row[14]
                obj["depVariance"] = row[15]
                obj["arrVariance"] = row[16]
                obj["internationalFlag"] = row[17]
                dataSet.append(obj)
            count = count + 1
    return dataSet


def consitencyCheck():
    types = {
        "airline": [],
        "origin": [],
        "aircraft": [],
        "depGate": [],
        "taxiOut": [],
        "depVariance": [],
        "internationalFlag": [],
        "destination": []
    }
    dataSet = readInCSV()
    for set in dataSet:
        if not (set["airline"] in types["airline"]):
            types["airline"].append(set["airline"])
        if not (set["origin"] in types["origin"]):
            types["origin"].append(set["origin"])
        if not (set["aircraft"] in types["aircraft"]):
            types["aircraft"].append(set["aircraft"])
        if not (set["depGate"] in types["depGate"]):
            types["depGate"].append(set["depGate"])
        if not (set["taxiOut"] in types["taxiOut"]):
            types["taxiOut"].append(set["taxiOut"])
        if not (set["depVariance"] in types["depVariance"]):
            types["depVariance"].append(set["depVariance"])
        if not (set["internationalFlag"] in types["internationalFlag"]):
            types["internationalFlag"].append(set["internationalFlag"])
        if not (set["destination"] in types["destination"]):
            types["destination"].append(set["destination"])

    print(types['aircraft'])

def dayCalculator(y, m, d):
    count = 0
    yy = int(y)
    mm = int(m)
    dd = int(d)
    if mm == 1:
        count = dd
    if mm == 2:
        count = dd + 31
    if mm == 3:
        count = dd + 59
    if mm == 4:
        count = dd + 90
    if mm == 5:
        count = dd + 120
    if mm == 6:
        count = dd + 151
    if mm == 7:
        count = dd + 181
    if mm == 8:
        count = dd + 212
    if mm == 9:
        count = dd + 243
    if mm == 10:
        count = dd + 273
    if mm == 11:
        count = dd + 304
    if mm == 12:
        count = dd + 334
    if yy == 2018:
        count = count + 365
    return count

# Week (1/1/17 is a Sunday)
def dayToWeekday(n):
    number = int(n)
    if number % 7 == 0:
        return "Saturday"
    else:
        if number % 7 == 1:
            return "Sunday"
        if number % 7 == 2:
            return "Monday"
        if number % 7 == 3:
            return "Tuesday"
        if number % 7 == 4:
            return "Wednesday"
        if number % 7 == 5:
            return "Thursday"
        if number % 7 == 6:
            return "Friday"

def  actDepartTimeFlag(time):
    if(time):
        t = int(time)
        # 12am to 4am
        if t >= 0 and t < 240:
            return "1"
        # 4am to 8am
        if t >= 240 and t < 480:
            return "2"
        # 8am to 12pm
        if t >= 480 and t < 720:
            return "3"
        # 12pm to 4pm
        if t >= 720 and t < 960:
            return "4"
        # 4pm to 8pm
        if t >= 960 and t < 1200:
            return "5"
        # 8pm to 12am
        if t >= 1200 and t < 1441:
            return "6"
    else:
        return "0"


def cleanDataOne():
    dataSet = readInCSV()
    newDataSet = []
    for set in dataSet:
        # Remove Gate
        if "Gate" in set["depGate"]:
            set["depGate"] = set["depGate"].replace("Gate ", "")


        # Remove leading 0 from Gate
        if set["depGate"] and "0" in set["depGate"][0]:
            set["depGate"] = set["depGate"][0].replace("0", "")

        # Change Null departure Gates to 0
        if "NULL" in set["depGate"] or not set["depGate"]:
            set["depGate"] = "0"

        # Remove letters from Gates
        if not set["depGate"].isdigit() and not set["depGate"] == "1A":
            s = [int(s) for s in re.findall(r'-?\d+\.?\d*', set["depGate"])]
            set["depGate"] = s[0]
        if set["depGate"] == "1A":
            set["depGate"] = "52"

        # Change Airline to Number
        if not set["airline"]:
            set["airline"] = "0"
        else:
            if set["airline"] == "AC":
                set["airline"] = "1"
            if set["airline"] == "WN":
                set["airline"] = "2"
            if set["airline"] == "AS":
                set["airline"] = "3"
            if set["airline"] == "DL":
                set["airline"] = "4"
            if set["airline"] == "AA":
                set["airline"] = "5"
            if set["airline"] == "NK":
                set["airline"] = "6"
            if set["airline"] == "VX":
                set["airline"] = "7"
            if set["airline"] == "SY":
                set["airline"] = "8"
            if set["airline"] == "B6":
                set["airline"] = "9"
            if set["airline"] == "WS":
                set["airline"] = "10"
            if set["airline"] == "F9":
                set["airline"] = "11"
            if set["airline"] == "HA":
                set["airline"] = "12"
            if set["airline"] == "G4":
                set["airline"] = "13"
            if set["airline"] == "UA":
                set["airline"] = "14"

        # Change Aircraft to Number
        if not set["aircraft"]:
            set["aircraft"] = "NULL"
        else:
            if set["aircraft"] == "32S":
                set["aircraft"] = "1"
            if set["aircraft"] == "737":
                set["aircraft"] = "2"
            if set["aircraft"] == "EMJ":
                set["aircraft"] = "3"
            if set["aircraft"] == "DH8":
                set["aircraft"] = "4"
            if set["aircraft"] == "CRJ":
                set["aircraft"] = "5"
            if set["aircraft"] == "M90":
                set["aircraft"] = "6"
            if set["aircraft"] == "757":
                set["aircraft"] = "7"
            if set["aircraft"] == "330":
                set["aircraft"] = "8"
            if set["aircraft"] == "767":
                set["aircraft"] = "9"
            if set["aircraft"] == "M80":
                set["aircraft"] = "10"
            if set["aircraft"] == "717":
                set["aircraft"] = "11"
            if set["aircraft"] == "E75":
                set["aircraft"] = "12"
            if set["aircraft"] == "NULL":
                set["aircraft"] = "0"


        # Break Up Date and Time
        if set["schDepartTime"]:
            set['fullSchDate'] = set["schDepartTime"]
            set["schDepartDate"], set["schDepartTime"] = set["schDepartTime"].replace("\"", "").split(" ")
        else:
            set["schDepartDate"], set["schDepartTime"] = 0, 0
            set['fullSchDate'] = 0
        if set["actualDepartTime"]:
            set["actualDepartDate"], set["actualDepartTime"] = set["actualDepartTime"].replace("\"", "").split(" ")
        else:
            set["actualDepartDate"], set["actualDepartTime"] = 0, 0

        # #Round min to nearest 15
        if set["schDepartTime"]:
            s = set["schDepartTime"].split(":")
            m = 15 * round(int(s[1]) / 15)
            set["schDepartTime"] = s[0] + ":" + str(m) + ":" + s[2]
        if set["actualDepartTime"]:
            s = set["actualDepartTime"].split(":")
            m = 15 * round(int(s[1]) / 15)
            set["actualDepartTime"] = s[0] + ":" + str(m) + ":" + s[2]


        # # Change Time to Number and Round
        if set["schDepartTime"]:
            s = set["schDepartTime"].split(":")
            set["schDepartTime"] = (int(s[0]) * 60) + 15 * round(int(s[1]) / 15)
        if set["actualDepartTime"]:
            s = set["actualDepartTime"].split(":")
            set["actualDepartTime"] = (int(s[0]) * 60) + 15 * round(int(s[1]) / 15)

        # # Add time of day flag
        set['todFlag'] = actDepartTimeFlag(set["actualDepartTime"])

        # Change Date to Number
        if(set["actualDepartDate"]):
            y, m, d = set["actualDepartDate"].split("-")
            set["actualDepartDate"] = dayCalculator(y, m, d)
            set["actualMonth"] = m
        else:
            set["actualDepartDate"] = 0
        if(set["schDepartDate"]):
            y, m, d = set["schDepartDate"].split("-")
            set["schDepartDate"] = dayCalculator(y, m, d)
            set["schMonth"] = str(m)

        # Add Day of Week (1/1/17 is a Sunday)
        set["weekday"] = dayToWeekday(set["actualDepartDate"])

        # Remove Null taxi time and add set
        if set["taxiOut"] and (set["depGate"] == '1A' or int(set["depGate"]) <= 52):
            # if int(set["actualDepartDate"]) >= 0 and int(set["actualDepartDate"]) <= 90:
            # if int(set["actualDepartDate"]) >= 365 and int(set["actualDepartDate"]) <= 455:
                if int(set["taxiOut"]) >= 6 and int(set["taxiOut"]) <= 40:
                    # if set["airline"] == '3':
                        newDataSet.append(set)

    return newDataSet


# Write out clean data
def writeCleanedData():
    dataSet = cleanDataOne()
    with open('cleanDataForML8.csv', 'w', newline='\n') as csvfile:
            fieldnames = [
                'airline',
                "aircraft",
                "depGate",
                "weekday",
                "schDepartTime",
                "schMonth",
                "schDepartDate",
                "actualDepartTime",
                "actualDepartDate",
                "taxiOut",
                "internationalFlag",
                "flightNumber",
                "monthDayTime"
                "fullSchDate"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for set in dataSet:
                writer.writerow({
                    "flightNumber": set["airline"] + str(set['flightNumber']),
                    'airline': set["airline"],
                    'aircraft': set["aircraft"],
                    'fullSchDate': set["fullSchDate"].replace("\"", ""),
                    "flightNumber": set["airline"] + str(set["flightNumber"]),
                    "depGate": "G" + str(set["depGate"]),
                    "weekday": set["weekday"],
                    "schDepartTime": set["schDepartTime"].replace("\"", ""),
                    "monthDayTime": set["schMonth"]+":"+set["weekday"]+":"+str(set["schDepartTime"]),
                    "schMonth": set["schMonth"],
                    "schDepartDate": set["schDepartDate"],
                    "actualDepartTime": set["actualDepartTime"].replace("\"", ""),
                    "actualDepartDate": set["actualDepartDate"],
                    "todFlag": set["todFlag"],
                    "taxiOut": set["taxiOut"],
                    "depVariance": set["depVariance"],
                    "internationalFlag": set["internationalFlag"]
                })


writeCleanedData()