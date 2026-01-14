FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/
COPY checker/utils/timer/timer.py /app/timer.py

ENTRYPOINT ["python3", "/app/timer.py"]
