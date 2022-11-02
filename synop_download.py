#Ogimet.com latest synop scraper
#Made by: SvenAzari

import requests
import re
import os
import datetime
from datetime import timezone

#How to set up:
#  1. Use https://ogimet.com/usynops.phtml.en to choose country 
#  2. Choose tekst format.
#  3. After opening query, copy url.
#  4. Do not forget to uncomment 4 lines if you wanna write scraped lines into file!

#grabbing data

url = "https://ogimet.com/ultimos_synops2.php?lang=en&estado=Croa&fmt=txt&Send=Send" #paste url here (current url is for Croatia)
r = requests.get(url, allow_redirects=True)
open('latest_synop.txt', 'wb').write(r.content) #writing content of webpage into file

#scraping data

synop = open ("latest_synop.txt") #openning file where content of webpage is saved

#search for <pre> and </pre> tags
lookup1 = "<pre>"
lookup2 = "</pre>"

#look for line of beginning tag
with open("latest_synop.txt") as myFile:
    for numx, line in enumerate(myFile, 1):
        if lookup1 in line:
            x = numx
            
#look for line of ending tag
with open("latest_synop.txt") as myFile:
    for numy, line in enumerate(myFile, 1):
        if lookup2 in line:
            y = numy

lines_to_read = range (x+7, y-1) #lines to scrap

dt = datetime.datetime.now(timezone.utc) #utc time
hourutc = str(dt.hour) #utc hour

linesx = [] #list where lines are saved

for position, line in enumerate(synop):
    if position in lines_to_read:
        linesx.append(line) #add lines to list
        
linesy = "".join(linesx) #all lines in one giant string
linesnew = linesy.split("=\n") #split linesy

#printing or saving data

syn = open("/home/azari/scripts/synop.txt", "w+") #creating and opening file to write scraped lines into (uncomment to use - 1/4)

c = 0

while True:
    try:
        synop = linesnew[0+c] #new string for each report
        synopx = re.split(' |\n', synop) #split last line string to list
        while("" in synopx): #remove unnecessary spaces
            synopx.remove("")
        del synopx[0]
        timex = synopx[1]
        time = timex[2:4] #time of report
        indexx = synopx[3]
        index = indexx [1:2] #station describer index
        if float(time) == float(hourutc) and (index == "1" or index == "2" or index == "3"): #print or save line only if observation was made by human and if report is not for some of previouse hours
            synopprint = " ".join(synopx)
#            print(synopprint.replace("=",'')) #print scraped lines on screen - put under comment if you won't use this
            syn.write(synopprint.replace("=",'')) #write scraped lines to file - uncomment this to use (2/4)
            syn.write('==\n') #(3/4)
            synopx.clear()
            c += 1
            continue
        else: #discard other synop reports
            synopx.clear()
            c += 1
            continue
    except IndexError:
        synopx.clear()
        break

syn.close() #closing file where lines are written - uncomment this to use (4/3)
       
os.remove("latest_synop.txt") #removing file where web page content is written
        

