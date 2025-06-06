FROM python:3.10-slim
WORKDIR /opt/render/project/src
COPY . .
RUN pip install -r requirements.txt
ENV PORT=10000
EXPOSE 10000
CMD ["python3", "bot.py"]
