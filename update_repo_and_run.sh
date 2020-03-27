#!/bin/bash

cd ~/Documents/covid19/covid19
ls

#1 go to data repo and get latest data
cd ~/Documents/covid19/COVID-19
git status
git pull -p

git log --oneline -5 > ~/Documents/covid19/covid19/curr_data_master.txt

pwd

#2 go back to main repo and run
cd ~/Documents/covid19/covid19
python3 covid19.py

git add *
git commit -m "daily update"
git push
