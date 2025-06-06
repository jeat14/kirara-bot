FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 uninstall -y python-telegram-bot  # Uninstall any existing version
RUN pip3 install --no-cache-dir -r requirements.txt # Fresh install

COPY . .

CMD ["python3", "kirara_bot.py"]
