Database migrate command
:~ python -m app.init_db

Open Command Prompt as Administrator
Run the Uvicorn Command:
:~ uvicorn app.main:app --host 0.0.0.0 --port 80