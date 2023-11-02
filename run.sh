#!/bin/bash

cd account 
python -m uvicorn service:app --port 8081 --reload > account.log.txt &


cd .. 
cd artists
python -m uvicorn service:app --port 8003 --reload > artists.log.txt &


cd ..
cd tracks
python -m uvicorn service:app --port 8002 --reload > tracks.log.txt &


cd ..
cd albums
python -m uvicorn service:app --port 8001 --reload > albums.log.txt &


cd ..
python rabbitmq.sh > rabbitmq.log.txt &


echo "Starting..."


