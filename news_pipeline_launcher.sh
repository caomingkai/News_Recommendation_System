#!/bin/bash

# start redis
redis-server &

# start mongodb
sudo mongod &

pip install -r requirements.txt

cd backend_server
python service.py &

cd ../news_pipeline
python news_monitor.py &
python news_fetcher.py &
python news_deduper.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
