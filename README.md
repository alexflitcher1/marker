# Marker
Marker is music streaming like Yandex Music

## Installation
Download requirements:

`pip install requirements.txt`

Install the packages ` postgresql` and `rabbitmq`

**Arch Linux:**

`sudo pacman -S postgresql rabbitmq`

In postgresql create databases: *accounts, albums, artists, tracks*

Update connection string in */db.py scripts and 
run */db.py scripts

## Deploy

Run `run.sh` script