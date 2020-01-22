c:
cd \apps\abbui-app
SET SESSION_COOKIE_NAME=abbui-app
SET SESSION_HOST=localhost
SET SESSION_PORT=27017
SET SESSION_DB=session
.\venv\scripts\waitress-serve --host=0.0.0.0 --port=6020 app:app
