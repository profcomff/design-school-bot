FROM python:3.10
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

ADD bot /app/bot

CMD [ "python3", "-m", "bot"]
