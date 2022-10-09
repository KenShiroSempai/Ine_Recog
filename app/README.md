# Entorno virtual para fastApi
para crear el entorno en otra computadora:
python3 -m venv .fastApi

para activarlo:
source .fastApi/bin/activate

uvicorn main:app --host 192.168.100.140 --port 4999