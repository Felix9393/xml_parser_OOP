import xml.etree.ElementTree as ET
#For a better description of the library you may want to have a look at this manual
#https://docs.python.org/3/library/xml.etree.elementtree.html
import os
import sys
import csv

class XML_Parser():
    #define the basic local vaiables
    def __init__(self, file_name):
        self.tree = ET.parse(file_name)
        self.root = self.tree.getroot()             
        self.file_name = file_name

    #the actual xml parser
    def parse(self, ts):
        self.counter = 0
        self.ts = ts
        #during the first loop set the columnnames for the csv file
        for neighbor in self.root.iter('trkseg'):
            for child in neighbor.findall('trkpt'):
                if self.counter == 0:
                    #create a new trkpt() object and append it to the trkseg() object
                    trackpt = trkpt()
                    self.ts.trkpt.append(trackpt)
                    self.ts.trkpt[0].lat = 'lat'
                    self.ts.trkpt[0].lon = 'lon'
                    self.ts.trkpt[0].ele = child.find('ele').tag
                    self.ts.trkpt[0].time = child.find('time').tag
                    for subchild in child.findall('extensions'):
                        #create a new extensions() object and append it to the trkpt() object
                        extens = extensions()
                        self.icounter = 0
                        self.ts.trkpt[0].extension.append(extens)
                        self.ts.trkpt[0].extension[self.icounter].distance = subchild.find('distance').tag
                        self.ts.trkpt[0].extension[self.icounter].speed = subchild.find('speed').tag
                        self.ts.trkpt[0].extension[self.icounter].course = subchild.find('course').tag
                        self.ts.trkpt[0].extension[self.icounter].acceleration = subchild.find('acceleration').tag
                        self.icounter += 1
                    self.counter += 1
                #here the data will be added below the columnnames
                trackpt = trkpt()
                self.ts.trkpt.append(trackpt)
                self.ts.trkpt[self.counter].lat = child.get('lat')
                self.ts.trkpt[self.counter].lon = child.get('lon')
                self.ts.trkpt[self.counter].ele = child.find('ele').text
                self.ts.trkpt[self.counter].time = child.find('time').text
                for subchild in child.findall('extensions'):
                        extens = extensions()
                        self.icounter = 0
                        self.ts.trkpt[self.counter].extension.append(extens)
                        self.ts.trkpt[self.counter].extension[self.icounter].distance = subchild.find('distance').text
                        self.ts.trkpt[self.counter].extension[self.icounter].speed = subchild.find('speed').text
                        self.ts.trkpt[self.counter].extension[self.icounter].course = subchild.find('course').text
                        self.ts.trkpt[self.counter].extension[self.icounter].acceleration = subchild.find('acceleration').text
                        self.icounter += 1
                self.counter += 1

    #this function takes the data parsed and writes 
    def csv_writer(self):
        new_name = os.path.splitext(self.file_name)[0]
        with open(new_name + '.txt', 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = ',')
            for i, dicts in enumerate(self.ts.trkpt):
                csv_writer.writerow([self.ts.trkpt[i].lat,self.ts.trkpt[i].lon,self.ts.trkpt[i].ele,self.ts.trkpt[i].time,self.ts.trkpt[i].extension[0].distance,self.ts.trkpt[i].extension[0].speed,self.ts.trkpt[i].extension[0].course,self.ts.trkpt[i].extension[0].acceleration])

class trkseg():
    def __init__(self):
        self.trkpt = []

class trkpt():
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.ele = 0
        self.time = 0
        self.extension = []
    
class extensions():
    def __init__(self):
        self.distance = 0
        self.speed = 0
        self.course = 0
        self.acceleration = 0

def find_all_files():
    mylist = []
    for file in os.listdir(os.path.dirname(sys.argv[0])):
        if file.endswith(".xml"):
            mylist.append(file)
    return mylist
        
def main():
    #Set any directory desired, here the directory of this file will be used
    os.chdir(os.path.dirname(sys.argv[0]))
    trackseg = trkseg()
    filelist = find_all_files()
    for file in filelist:
        my_parser = XML_Parser(file)
        my_parser.parse(trackseg)
        print('Writing')
        my_parser.csv_writer()

if __name__ == '__main__':
    main()
    
