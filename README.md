# Hotel

## Quick start

- Create your .env file. You can use copy of .env.example
- Use `python3 -m venv ./.venv && source ./.venv/bin/activate && pip install -r requirements.txt`
- Run `docker compose up -d --build`
- Run `docker exec app alembic upgrade head`
- API docs - `http://localhost:8000/docs`
