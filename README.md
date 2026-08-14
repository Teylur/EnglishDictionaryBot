# Project Initialisation

pip install -r requirements.txt

## Запуск фронтенда сейчас:

python -m front.main

## Backend:

postgresql:

docker run -v path:/var/lib/postgresql --name pg_container -e POSTGRES_PASSWORD=admin -d -p 15432:5432 postgres

ollama:

ollama run qwen2.5:3b

## News:

Next: Refactore the back part, make more connection between front and back, and connect database ( if you can ) Completed

Next: start using a third-party api for translate and generating examples, make opportunity to see a word list and delete a word. Copleted

Next: add examples.