FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8090

CMD ["gunicorn", "-b", "0.0.0.0:8090", "futurebase.wsgi:application"]
