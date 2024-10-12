FROM  python:3.8-slim
WORKDIR /detrModel
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
COPY model/ .
CMD ["python", "./model.py"]