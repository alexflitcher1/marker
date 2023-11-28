# Marker
Marker is music streaming like Yandex Music

## Installation
Download requirements:

`pip install requirements.txt`

Goes to `gateway` folder

`npm i`

Install the packages ` postgresql` and `rabbitmq` also `nodejs` `npm`

**Arch Linux:**

`sudo pacman -S postgresql rabbitmq nodejs npm`

In postgresql create databases: *accounts, albums, artists, tracks*

Update connection string in */db.py scripts and 
run */db.py scripts

## Deploy

Run `run.sh` script

In `gateway` folder
`npm start`