FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

EXPOSE 8090

CMD ["gunicorn", "-b", "0.0.0.0:8090", "futurebase.futurebase.wsgi:application"]
