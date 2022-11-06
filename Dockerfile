FROM python:3.10
WORKDIR /app
RUN mkdir -p static

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

ADD bot /app/bot

CMD [ "python3", "-m", "bot"]
