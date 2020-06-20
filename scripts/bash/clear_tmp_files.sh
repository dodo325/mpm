#!/bin/sh
find . -name "__pycache__" -type d -exec rm -r "{}" \;
find . -name ".tox" -type d -exec rm -r "{}" \; 
find . -name ".pytest_cache" -type d -exec rm -r "{}" \; 
find . -name "*.egg-info" -type d -exec rm -r "{}" \; 
find . -name "mpm.egg-info" -type d -exec rm -r "{}" \; 

read -p "Remove dist? (y/n) " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    find . -name "dist" -type d -exec rm -r "{}" \;    
    find . -name "build" -type d -exec rm -r "{}" \;    
fi
