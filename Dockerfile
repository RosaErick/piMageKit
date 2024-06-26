FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000


ENV FLASK_RUN_HOST=0.0.0.0


CMD ["flask", "run"]

