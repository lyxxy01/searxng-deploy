FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir gunicorn flask baidu-search
COPY app.py .
EXPOSE $PORT
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
