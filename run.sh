#!/bin/bash

cd account 
python3 -m uvicorn service:app --port 8081 --reload > account.log.txt &


cd .. 
cd artists
python3 -m uvicorn service:app --port 8003 --reload > artists.log.txt &


cd ..
cd tracks
python3 -m uvicorn service:app --port 8002 --reload > tracks.log.txt &


cd ..
cd albums
python3 -m uvicorn service:app --port 8001 --reload > albums.log.txt &

cd ..
cd cdn
python3 -m uvicorn service:app --port 8004 --reload > cdn.log.txt &

cd ..
cd search
python3 -m uvicorn service:app --port 8005 --reload > search.log.txt &

cd ..
cd playlists
python3 -m uvicorn service:app --port 8006 --reload > playlists.log.txt &

cd ..
python3 rabbitmq.py > rabbitmq.log.txt &


echo "Starting..."


