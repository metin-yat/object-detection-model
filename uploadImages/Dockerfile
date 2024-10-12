FROM python:3.8-slim
WORKDIR /website
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY website/ .
EXPOSE 5000
CMD ["python", "./main.py"]