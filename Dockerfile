FROM python:3.10.12-alpine

WORKDIR /opt/backend_app

COPY . /opt/backend_app

RUN pip install Flask==3.0.0 Flask-Cors==3.0.10 Werkzeug==3.0.1 PyMySQL==1.1.0 cryptography==40.0.2


EXPOSE 5001


CMD ["sh", "-c", "nohup python3 rest_app.py &"]
