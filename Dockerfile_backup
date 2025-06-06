FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY kirara_bot.py .
ENV PORT=10000
EXPOSE 10000
CMD ["python", "kirara_bot.py"]
