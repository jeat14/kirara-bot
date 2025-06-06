FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY kirara_bot.py .
CMD ["python", "kirara_bot.py"]
