#!/bin/bash

#all file locatons need to be set for your case

python3 /home/$(whoami)/scripts/synop_download.py #run scrapper bot
wait #wait till all operations are done and then continue

folim=$(date -u +"%Y%m") #folder name for year and month
folim2=$(date -u +"%m%d") #folder name for month and day

#check if all folder exist - if do not, create them
[[ ! -d /home/$(whoami)/other_data/saved_synop/$folim ]] && mkdir /home/$(whoami)/other_data/saved_synop/$folim
[[ ! -d /home/$(whoami)/other_data/saved_synop/$folim/$folim2 ]] && mkdir /home/$(whoami)/other_data/saved_synop/$folim/$folim2

FILE=/home/$(whoami)/scripts/synop.txt #file which will be copied 
dattim=$(date -u +"%Y%m%d%H") #file name after copying
if [ -s "$FILE" ]; then #check if file which needs to be copied exist and has size greater than zero - if does, copy it
  cp $FILE /home/$(whoami)/other_data/saved_synop/$folim/$folim2/synop_hr_$dattim.txt
  rm $FILE
else
  exit
fi
