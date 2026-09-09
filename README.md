# Project Initialisation

pip install -r requirements.txt

## Запуск фронтенда сейчас:

python -m front.main

## Backend:

postgresql:

docker run -v path:/var/lib/postgresql --name pg_container -e POSTGRES_PASSWORD=admin -d -p 15432:5432 postgres

ollama:

ollama run qwen2.5:3b

redis:

docker run -d --name engbot-redis -p 6379:6379 redis

FastAPI:

uvicorn src.main:app

## News:

Next: Refactore the back part, make more connection between front and back, and connect database ( if you can ) Completed

Next: start using a third-party api for translate and generating examples, make opportunity to see a word list and delete a word. Completed

Next: add examples. Completed

added: worked word_list, word_create, word_delete. translate and examples in right way(by get), if word is already exists then we don't ask qwen just pull these info from database

Next: Remake whole backend to async completed

added: redis easy cache system. 

added: game system, it uses redis cache.