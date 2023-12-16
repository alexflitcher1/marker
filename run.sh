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
cd cdn
python -m uvicorn service:app --port 8004 --reload > cdn.log.txt &

cd ..
cd search
python -m uvicorn service:app --port 8005 --reload > search.log.txt &

cd ..
cd playlists
python -m uvicorn service:app --port 8006 --reload > playlists.log.txt &

cd ..
python rabbitmq.py > rabbitmq.log.txt &


echo "Starting..."


