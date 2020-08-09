#!/usr/bin/bash
python3.6 -m venv FactBot
mv requirements.txt FactBot/
mv bot.py FactBot/
mv token.txt FactBot/
touch ./FactBot/stats.json
echo "{\"lastID\": 0}" > ./FactBot/stats.json
mkdir FactBot/facts
mkdir FactBot/logs
mkdir FactBot/backup
chmod +x FactBot/bin/activate
. FactBot/bin/activate
pip install -r FactBot/requirements.txt