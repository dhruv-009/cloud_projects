FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY index.py .

EXPOSE 7001

CMD ["python", "index.py"]